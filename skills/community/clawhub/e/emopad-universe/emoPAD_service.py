#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情绪PAD计算常驻服务（多模态版）
整合 EEG、PPG、GSR，使用完整特征提取和 PAD 映射，提供 HTTP API
"""

import asyncio
import threading
import time
import queue
import numpy as np
from collections import deque
import struct
import json
import os
import sys
from datetime import datetime
import logging
import warnings
import re
from typing import Optional

# 硬件接口
import serial
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

# 信号处理
import mne
import heartpy as hp
import neurokit2 as nk
from scipy import signal
from scipy.signal import find_peaks, butter, filtfilt, welch
from scipy.ndimage import uniform_filter1d
import pywt

# 可视化（离屏）
import pyvista as pv

# Web 服务
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
import io
from PIL import Image
from heartpy.exceptions import BadSignalWarning
try:
    import asrpy
    ASR_AVAILABLE = True
except ImportError:
    ASR_AVAILABLE = False
    asrpy = None
    warnings.warn("asrpy 未安装，将禁用 ASR 伪影去除。请运行: pip install asrpy")

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== 熵函数（来自原文件） ====================
def sample_entropy(signal, m=2, r=None):
    if r is None:
        r = 0.2 * np.std(signal)
    N = len(signal)
    if N < m + 1:
        return 0.0
    def _maxdist(xi, xj):
        return max(np.abs(xi - xj))
    def _phi(m):
        templates = [signal[i:i+m] for i in range(N - m + 1)]
        count = 0
        for i in range(len(templates)):
            for j in range(len(templates)):
                if i != j and _maxdist(templates[i], templates[j]) <= r:
                    count += 1
        if len(templates) <= 1:
            return 0
        return count / (len(templates) * (len(templates) - 1))
    phi_m = _phi(m)
    phi_m1 = _phi(m+1)
    if phi_m == 0 or phi_m1 == 0:
        return 0
    return -np.log(phi_m1 / phi_m)

def permutation_entropy(signal, m=3, delay=1):
    n = len(signal)
    if n < m:
        return 0.0
    patterns = {}
    for i in range(n - (m-1)*delay):
        idx = np.argsort(signal[i:i+m*delay:delay])
        pattern = tuple(idx)
        patterns[pattern] = patterns.get(pattern, 0) + 1
    total = sum(patterns.values())
    probs = [c/total for c in patterns.values()]
    return -sum(p * np.log(p) for p in probs)

# ==================== KSEEG102 Handler（来自原文件） ====================
class KSEEG102Handler:
    SERVICE_UUID = "8653000a-43e6-47b7-9cb0-5fc21d4ae340"
    CONTROL_UUID = "8653000c-43e6-47b7-9cb0-5fc21d4ae340"
    DATA_UUID    = "8653000b-43e6-47b7-9cb0-5fc21d4ae340"

    START_COMMAND_2BYTE = bytes([0xE3, 0x00])
    START_COMMAND_1BYTE = bytes([0xE3])
    START_COMMAND_ALT = bytes([0x01])
    STOP_COMMAND = bytes([0x00, 0x00])

    def __init__(self, client: BleakClient, sample_callback, scale=10000.0):
        self.client = client
        self.sample_callback = sample_callback
        self.scale = scale
        self._running = False
        self._raw_file = None
        self._heartbeat_task = None
        self._control_char = None
        self._notify_handles = []
        self._data_char = None
        # ---------- 新增：数据超时检测 ----------
        self.last_data_time = 0
        self.data_timeout = 10  # 秒，超过此时间无数据则尝试重新启动流

    async def start(self, raw_data_file: Optional[str] = None):
        self._running = True
        if raw_data_file:
            os.makedirs(os.path.dirname(raw_data_file) or '.', exist_ok=True)
            self._raw_file = open(raw_data_file, 'wb')
            logger.info(f"Logging raw data to: {raw_data_file}")

        # 1. 先发现通知特征
        notify_chars = await self._discover_notify_characteristics()
        # 2. 启用通知（先于启动命令，确保设备准备好发送数据）
        for char in notify_chars:
            try:
                await self.client.start_notify(char, self._on_data)
                logger.info(f"Started notifications on {char.uuid}")
                self._notify_handles.append(char)
                if char.uuid.lower() == self.DATA_UUID.lower():
                    self._data_char = char
            except Exception as e:
                logger.error(f"Failed to start notifications on {char.uuid}: {e}")

        if not self._notify_handles:
            raise RuntimeError("Could not start any notification")

        # 3. 尝试交换MTU，可能会触发连接参数协商
        try:
            await self.client.exchange_mtu(512)
            logger.info("Exchanged MTU to 512")
        except Exception as e:
            logger.debug(f"MTU exchange failed (non-critical): {e}")

        # 4. 发送启动命令
        await self._send_start_commands()

        logger.info(f"KSEEG102: {len(self._notify_handles)} notification characteristics active")
        self._heartbeat_task = asyncio.create_task(self._heartbeat())
        return True

    async def _discover_notify_characteristics(self) -> list:
        notify_chars = []
        logger.info("--- 服务列表 ---")
        for service in self.client.services:
            logger.info(f"Service: {service.uuid}")
            for char in service.characteristics:
                props = ", ".join(char.properties)
                logger.info(f"  Char: {char.uuid} [{props}]")
                if "notify" in char.properties:
                    notify_chars.append(char)
                if char.uuid == self.CONTROL_UUID:
                    self._control_char = char
                    logger.info(f"    -> Control characteristic found, max_write_without_response_size: {char.max_write_without_response_size}")
        logger.info(f"Found {len(notify_chars)} notify characteristics.")
        return notify_chars

    async def _send_start_commands(self):
        if not self._control_char:
            logger.warning("Control characteristic not found, skipping start commands.")
            return

        # 只发送最有可能有效的启动命令（可根据需要调整）
        commands = [
            ("2-byte start", self.START_COMMAND_2BYTE),
            # ("1-byte start", self.START_COMMAND_1BYTE),  # 如果2-byte有效可省略
        ]
        max_write = self._control_char.max_write_without_response_size
        logger.info(f"Control characteristic max write length: {max_write}")

        for name, cmd in commands:
            if len(cmd) > max_write:
                logger.warning(f"Command {name} length {len(cmd)} > max write length {max_write}, skipping")
                continue
            try:
                logger.info(f"Trying {name} (len={len(cmd)}): {cmd.hex()}")
                await self.client.write_gatt_char(self._control_char, cmd, response=False)
                logger.info(f"  -> {name} sent successfully (no response)")
            except Exception as e:
                logger.warning(f"  -> {name} failed (no response): {e}")
                try:
                    await self.client.write_gatt_char(self._control_char, cmd, response=True)
                    logger.info(f"  -> {name} sent successfully (with response)")
                except Exception as e2:
                    logger.warning(f"  -> {name} failed (with response): {e2}")
            await asyncio.sleep(0.5)

        # 可选：读取控制特征确认状态
        try:
            value = await self.client.read_gatt_char(self._control_char)
            logger.info(f"Control characteristic read: {value.hex()}")
        except Exception as e:
            logger.warning(f"Failed to read control characteristic: {e}")

    async def _heartbeat(self):
        """心跳任务：保持连接活跃并检测数据超时"""
        while self._running:
            await asyncio.sleep(2)  # 每2秒执行一次

            # 1. 发送一个空包（或保持命令）以维持连接
            try:
                if self._control_char:
                    # 写入空包（某些设备通过空包维持连接）
                    await self.client.write_gatt_char(self._control_char, b'', response=False)
                    logger.debug("Heartbeat sent (empty packet)")
            except Exception as e:
                logger.warning(f"Heartbeat write failed: {e}")

            # 2. 检查数据超时
            if time.time() - self.last_data_time > self.data_timeout:
                logger.warning("Data timeout detected, restarting data stream...")
                try:
                    await self._send_start_commands()
                except Exception as e:
                    logger.error(f"Restart failed: {e}")

    async def stop(self):
        self._running = False
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass

        # 停止所有通知
        for char in self._notify_handles:
            try:
                await self.client.stop_notify(char)
                logger.info(f"Stopped notifications on {char.uuid}")
            except Exception as e:
                logger.warning(f"Failed to stop notifications on {char.uuid}: {e}")

        # 发送停止命令
        if self._control_char:
            try:
                await self.client.write_gatt_char(self._control_char, self.STOP_COMMAND, response=False)
                logger.info("Stop command sent")
            except Exception as e:
                logger.warning(f"Failed to send stop command: {e}")

        if self._raw_file:
            self._raw_file.close()

    def _on_data(self, sender: BleakGATTCharacteristic, data: bytes):
        # 更新最后数据时间
        self.last_data_time = time.time()

        char_uuid = sender.uuid.lower()
        if self._raw_file:
            ts = time.time()
            self._raw_file.write(struct.pack('<d', ts))
            self._raw_file.write(len(data).to_bytes(2, 'little'))
            self._raw_file.write(data)
            self._raw_file.flush()

        logger.debug(f"Data from {char_uuid}: length={len(data)}, hex={data[:20].hex()}...")

        if char_uuid == self.DATA_UUID.lower() and len(data) == 69:
            self._parse_eeg_binary(data)
            return
        elif char_uuid == self.DATA_UUID.lower():
            logger.warning(f"Data from data characteristic with unexpected length {len(data)}")
            return

        # 处理其他可能的特征（如未知服务）
        if char_uuid == "da2e7828-fbce-4e01-ae9e-261174997c48":
            logger.info(f"Data from unknown service: {data.hex()}")
            return

        # 尝试解析为JSON文本
        try:
            text = data.decode('utf-8').strip()
            if text:
                obj = json.loads(text)
                logger.info(f"JSON data: {obj}")
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass

    def _parse_eeg_binary(self, data: bytes):
        if len(data) != 69:
            return
        payload = data[5:69]
        if len(payload) != 64:
            return

        samples = []
        for i in range(0, 64, 2):
            val = int.from_bytes(payload[i:i+2], byteorder='little', signed=True)
            samples.append(val)

        ch1 = samples[0::2]
        ch2 = samples[1::2]

        if len(ch1) == 16 and len(ch2) == 16:
            ch1_scaled = [v / self.scale for v in ch1]
            ch2_scaled = [v / self.scale for v in ch2]
            timestamp = time.time()
            for v1, v2 in zip(ch1_scaled, ch2_scaled):
                self.sample_callback(timestamp, v1, v2)
            logger.debug(f"Parsed EEG packet: 16 samples each channel")

# ==================== 串口读取器（修改为直接回调） ====================
class SerialReader(threading.Thread):
    def __init__(self, port, baudrate, callback):
        super().__init__(daemon=True)
        self.port = port
        self.baudrate = baudrate
        self.callback = callback  # 函数签名 (timestamp, ppg, gsr)
        self.running = True

    def run(self):
        while self.running:
            try:
                ser = serial.Serial(self.port, self.baudrate, timeout=1)
                logger.info(f"串口 {self.port} 打开成功")
                while self.running:
                    try:
                        raw = ser.readline()
                        if not raw:
                            continue
                        line = raw.decode('utf-8', errors='replace').strip()
                        numbers = re.findall(r'-?\d+', line)
                        if len(numbers) >= 3:
                            filter_ppg, hrv, gsr_avg = map(int, numbers[:3])
                            timestamp = time.time()
                            self.callback(timestamp, filter_ppg, gsr_avg)
                            logger.debug(f"串口原始值: ppg={filter_ppg}, gsr={gsr_avg}")
                        else:
                            logger.debug(f"无法解析的行: {line}")
                    except Exception as e:
                        logger.error(f"串口读取/解析错误: {e}")
                        time.sleep(0.1)
                ser.close()
            except Exception as e:
                logger.error(f"无法打开串口 {self.port}: {e}，将在5秒后重试")
                time.sleep(5)
        logger.info("串口读取线程结束")

    def stop(self):
        self.running = False

# ==================== 多模态特征提取器（完整版） ====================
class MultimodalFeatureExtractor:
    def __init__(self, fs_eeg=256, fs_ppg=125, fs_gsr=100, use_wavelet=True):
        self.fs_eeg = fs_eeg
        self.fs_ppg = fs_ppg
        self.fs_gsr = fs_gsr
        self.use_wavelet = use_wavelet
        self.asr = None  # ASR对象，由外部设置
        self.asr_cutoff = 20

    def set_asr(self, asr, cutoff=20):
        """设置训练好的ASR对象"""
        self.asr = asr
        self.asr_cutoff = cutoff
        logger.info(f"ASR已设置 (cutoff={cutoff})，后续EEG数据将进行实时伪影去除")

    def wavelet_denoise(self, data, wavelet='db4', level=3, mode='soft'):
        denoised = np.zeros_like(data)
        for ch in range(data.shape[0]):
            coeffs = pywt.wavedec(data[ch], wavelet, level=level)
            sigma = np.median(np.abs(coeffs[-1])) / 0.6745
            threshold = sigma * np.sqrt(2 * np.log(len(data[ch])))
            coeffs_thresh = list(coeffs)
            for i in range(1, len(coeffs_thresh)):
                coeffs_thresh[i] = pywt.threshold(coeffs_thresh[i], threshold, mode=mode)
            denoised[ch] = pywt.waverec(coeffs_thresh, wavelet)[:len(data[ch])]
        return denoised

    def _calc_differential_entropy(self, power, eps=1e-12):
        return 0.5 * np.log(2 * np.pi * np.e * (power + eps))

    def _calc_bf_fhf(self, ppg, hr_mean, eps=1e-12):
        if hr_mean <= 30 or hr_mean >= 200:
            return 0.0, 0.0, 0.0

        hr_hz = hr_mean / 60.0
        nyquist = self.fs_ppg / 2

        bf_low = max(0.1, hr_hz - 0.3)
        bf_high = min(nyquist, hr_hz + 0.3)
        fhf_low = max(0.1, 2*hr_hz - 0.6)
        fhf_high = min(nyquist, 2*hr_hz + 0.6)

        if bf_high <= bf_low or fhf_high <= fhf_low:
            logger.debug(f"无效频带: BF [{bf_low:.2f}, {bf_high:.2f}], FHF [{fhf_low:.2f}, {fhf_high:.2f}]")
            return 0.0, 0.0, 0.0

        nperseg = min(512, len(ppg) // 2)
        nperseg = max(128, nperseg)
        f, pxx = welch(ppg, fs=self.fs_ppg, nperseg=nperseg, noverlap=nperseg//2)

        df = f[1] - f[0]
        bf_idx = np.logical_and(f >= bf_low, f <= bf_high)
        fhf_idx = np.logical_and(f >= fhf_low, f <= fhf_high)

        if not np.any(bf_idx) or not np.any(fhf_idx):
            logger.debug(f"频带内无频率点: BF any={np.any(bf_idx)}, FHF any={np.any(fhf_idx)}")
            return 0.0, 0.0, 0.0

        bf_power = np.trapz(pxx[bf_idx], dx=df)
        fhf_power = np.trapz(pxx[fhf_idx], dx=df)
        ratio = (bf_power / (fhf_power + eps)) if fhf_power > 0 else 0.0

        return bf_power, fhf_power, ratio
    
    def _compute_ppg_features_safe(self, ppg_array):
        """
        修复后的 PPG 特征提取 - 正确处理 HRV 频域特征
        输入: ppg_array - 原始 PPG 信号 (numpy 数组), 1分钟窗口
        返回: (features_dict, hr_mean, success_flag)
        """
        from heartpy.analysis import calc_fd_measures  # 正确导入
    
        features = {}
        hr_mean = 0.0
    
        try:
            # 1. 基础检查与清理
            ppg_clean = np.array(ppg_array, dtype=np.float64).flatten()
            if not np.all(np.isfinite(ppg_clean)):
                return None, 0.0, False
            if len(ppg_clean) < self.fs_ppg * 30:  # 至少30秒数据
                return None, 0.0, False
            if np.std(ppg_clean) < 1e-6:
                return None, 0.0, False
    
            # 2. HeartPy 带通滤波 (0.7 - 3.5 Hz，对应 42-210 BPM)
            filtered = hp.filter_signal(ppg_clean,
                                        cutoff=[0.7, 3.5],
                                        sample_rate=self.fs_ppg,
                                        order=3,
                                        filtertype='bandpass')
    
            # 3. 数据缩放
            scaled = hp.scale_data(filtered)
    
            # 4. 核心处理（峰值检测、RR 间期计算）
            wd, m = hp.process(scaled, sample_rate=self.fs_ppg,
                               report_time=False, clean_rr=True)
    
            # 5. 安全提取函数
            def safe_get(data_dict, key):
                val = data_dict.get(key, 0.0)
                return float(val) if np.isfinite(val) else 0.0
    
            hr_mean = safe_get(m, 'bpm')
            features['hr_mean'] = hr_mean
            features['hrv_rmssd'] = safe_get(m, 'rmssd')
            features['hrv_sdnn'] = safe_get(m, 'sdnn')
            features['hrv_sd1'] = safe_get(m, 'sd1')
            features['hrv_sd2'] = safe_get(m, 'sd2')
    
            if features['hrv_sd2'] > 1e-6:
                features['hrv_sd1_sd2'] = features['hrv_sd1'] / features['hrv_sd2']
            else:
                features['hrv_sd1_sd2'] = 0.0
    
            # 6. 频域特征 (LF/HF) - 修复后的正确调用方式
            try:
                # 检查是否有足够的 RR 间期
                if 'RR_list_cor' in wd and len(wd['RR_list_cor']) > 5:
                    # 对于1分钟数据，使用较小的 welch_wsize (30-60秒)
                    # 默认240秒会导致频率分辨率过低
                    welch_window = min(60, len(ppg_clean) / self.fs_ppg * 0.8)  # 使用窗口的80%
                    
                    # 抑制短信号警告（1分钟数据确实较短，但我们仍要计算）
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        wd, m = calc_fd_measures(
                            method='welch',
                            welch_wsize=welch_window,  # 关键：根据数据长度调整
                            square_spectrum=False,
                            measures=m,
                            working_data=wd
                        )
                    
                    features['hrv_lf'] = safe_get(m, 'lf')
                    features['hrv_hf'] = safe_get(m, 'hf')
                    features['hrv_lf_hf'] = safe_get(m, 'lf/hf')
                    
                    # 如果 lf/hf 计算失败，手动计算
                    if features['hrv_lf_hf'] == 0.0 and features['hrv_hf'] > 0:
                        features['hrv_lf_hf'] = features['hrv_lf'] / features['hrv_hf']
                else:
                    features['hrv_lf'] = 0.0
                    features['hrv_hf'] = 0.0
                    features['hrv_lf_hf'] = 0.0
                    
            except Exception as e:
                logger.debug(f"Frequency domain calculation failed: {e}")
                features['hrv_lf'] = 0.0
                features['hrv_hf'] = 0.0
                features['hrv_lf_hf'] = 0.0
    
            # 7. 结果合理性校验
            if 30 < hr_mean < 200:
                return features, hr_mean, True
            else:
                return None, 0.0, False
    
        except (BadSignalWarning, Exception) as e:
            logger.debug(f"HeartPy processing failed: {e}")
            return None, 0.0, False

    def _compute_ppg_features_fallback(self, ppg_array):
        """改进的备用 PPG 特征提取，使用 neurokit2 + scipy 组合"""
        try:
            # 1. 基础检查
            ppg_array = np.asarray(ppg_array, dtype=np.float64).flatten()
            if np.std(ppg_array) < 1e-6:
                return None, 0.0, False
    
            # 2. 使用 neurokit2 处理 PPG（推荐）
            signals, info = nk.ppg_process(ppg_array, sampling_rate=self.fs_ppg, method='elgendi')
            # 提取 HRV 特征
            hrv_indices = nk.hrv(signals['PPG_Rate'], sampling_rate=self.fs_ppg, show=False)
            if hrv_indices.empty:
                raise ValueError("Neurokit2 HRV failed")
    
            # 组装特征字典
            features = {}
            # 心率
            hr_mean = float(signals['PPG_Rate'].mean())
            features['hr_mean'] = hr_mean
    
            # HRV 时域
            features['hrv_rmssd'] = float(hrv_indices['HRV_RMSSD'].iloc[0]) if 'HRV_RMSSD' in hrv_indices else 0.0
            features['hrv_sdnn'] = float(hrv_indices['HRV_SDNN'].iloc[0]) if 'HRV_SDNN' in hrv_indices else 0.0
            features['hrv_sd1'] = float(hrv_indices['HRV_SD1'].iloc[0]) if 'HRV_SD1' in hrv_indices else 0.0
            features['hrv_sd2'] = float(hrv_indices['HRV_SD2'].iloc[0]) if 'HRV_SD2' in hrv_indices else 0.0
            if features['hrv_sd2'] > 1e-12:
                features['hrv_sd1_sd2'] = features['hrv_sd1'] / features['hrv_sd2']
            else:
                features['hrv_sd1_sd2'] = 0.0
    
            # HRV 频域（需 RR 间期）
            if 'HRV_LF' in hrv_indices:
                features['hrv_lf'] = float(hrv_indices['HRV_LF'].iloc[0])
                features['hrv_hf'] = float(hrv_indices['HRV_HF'].iloc[0])
                features['hrv_lf_hf'] = float(hrv_indices['HRV_LFHF'].iloc[0])
            else:
                features['hrv_lf'] = features['hrv_hf'] = features['hrv_lf_hf'] = 0.0
    
            return features, hr_mean, True
    
        except Exception as e:
            logger.debug(f"Neurokit2 PPG failed: {e}, falling back to scipy...")
    
        # 若 neurokit2 失败，回退到 scipy 方案（但可进一步优化）
        try:
            # 带通滤波（优化参数）
            nyquist = self.fs_ppg / 2
            low = 0.3 / nyquist   # 降低至 0.3 Hz
            high = 4.0 / nyquist
            b, a = butter(4, [low, high], btype='band')  # 4阶
            ppg_filtered = filtfilt(b, a, ppg_array)
    
            # 峰值检测（优化阈值）
            min_distance = int(0.4 * self.fs_ppg)  # 至少 0.4 秒间距
            height = np.percentile(ppg_filtered, 80)  # 使用高度阈值
            peaks, props = find_peaks(ppg_filtered, distance=min_distance,
                                      prominence=(None, None), height=height)
            if len(peaks) < 3:
                # 若峰值太少，尝试另一种 prominence 计算
                prom = 0.3 * (np.max(ppg_filtered) - np.min(ppg_filtered))
                peaks, _ = find_peaks(ppg_filtered, distance=min_distance, prominence=prom)
            if len(peaks) < 3:
                return None, 0.0, False
    
            # 后续计算 RR 间期、HRV 等（与原备用方案相同）
            # ...（此处省略重复代码，可沿用原备用方案）
            # 注意确保所有计算都有足够的 RR 间期
        except Exception as e:
            logger.debug(f"Scipy fallback also failed: {e}")
            return None, 0.0, False
    

    def extract(self, eeg_ch1, eeg_ch2, ppg, gsr):
        import time as time_module
        start_total = time_module.time()
        features = {}
        eps = 1e-12

        # ----- 信号截断 -----
        max_eeg_len = int(self.fs_eeg * 2)
        if len(eeg_ch1) > max_eeg_len:
            eeg_ch1 = eeg_ch1[-max_eeg_len:]
            eeg_ch2 = eeg_ch2[-max_eeg_len:]
            logger.debug(f"EEG数据截断至 {max_eeg_len} 点")
        max_ppg_len = int(self.fs_ppg * 60)
        if len(ppg) > max_ppg_len:
            ppg = ppg[-max_ppg_len:]
            logger.debug(f"PPG数据截断至 {max_ppg_len} 点")
        max_gsr_len = int(self.fs_gsr * 60)
        if len(gsr) > max_gsr_len:
            gsr = gsr[-max_gsr_len:]
            logger.debug(f"GSR数据截断至 {max_gsr_len} 点")

        # ----- 模态有效性判断 -----
        eeg_valid = (len(eeg_ch1) >= self.fs_eeg * 1.5 and len(eeg_ch2) >= self.fs_eeg * 1.5)
        ppg_valid = (len(ppg) >= self.fs_ppg * 3)
        gsr_valid = (len(gsr) >= self.fs_gsr * 2)
        logger.info(f"模态有效状态 - EEG: {eeg_valid}, PPG: {ppg_valid}, GSR: {gsr_valid}")

        # ---------- EEG 特征 ----------
        start_eeg = time_module.time()
        if eeg_valid:
            try:
                data = np.array([eeg_ch1, eeg_ch2])

                from mne.filter import filter_data, notch_filter
                data_filt = filter_data(data, self.fs_eeg, l_freq=0.5, h_freq=45, verbose=False,
                                         filter_length='auto', l_trans_bandwidth=0.5, h_trans_bandwidth=0.5, phase='zero')
                data_filt = notch_filter(data_filt, self.fs_eeg, freqs=50, verbose=False)

                # ===== 使用 ASRpy 进行实时伪影去除 =====
                if self.asr is not None and ASR_AVAILABLE:
                    try:
                        # 创建临时Raw对象
                        info = mne.create_info(ch_names=['ch1', 'ch2'], sfreq=self.fs_eeg, ch_types='eeg')
                        raw_tmp = mne.io.RawArray(data_filt, info)
                        # 应用ASR变换
                        raw_clean = self.asr.transform(raw_tmp)
                        data_filt = raw_clean.get_data()
                        logger.debug("ASRpy实时处理成功")
                    except Exception as e:
                        logger.warning(f"ASRpy实时处理失败，使用滤波后数据: {e}")
                # ===================================

                if self.use_wavelet:
                    data_filt = self.wavelet_denoise(data_filt)

                psds, freqs = mne.time_frequency.psd_array_welch(
                    data_filt, sfreq=self.fs_eeg, fmin=0.5, fmax=45,
                    n_fft=128, n_overlap=64, n_jobs=1, verbose=False
                )

                total_power = np.sum(psds, axis=-1, keepdims=True)
                rel_psds = psds / (total_power + eps)

                bands = {'delta': (0.5, 4), 'theta': (4, 8), 'alpha': (8, 13),
                         'beta': (13, 30), 'gamma': (30, 45)}
                for i, ch in enumerate(['ch1', 'ch2']):
                    for band_name, (low, high) in bands.items():
                        idx = np.logical_and(freqs >= low, freqs <= high)
                        band_power_abs = np.sum(psds[i, idx])
                        band_power_rel = np.sum(rel_psds[i, idx])
                        features[f'eeg_{ch}_{band_name}_abs'] = band_power_abs
                        features[f'eeg_{ch}_{band_name}'] = band_power_rel

                    for band_name in ['alpha', 'beta']:
                        low, high = bands[band_name]
                        idx = np.logical_and(freqs >= low, freqs <= high)
                        band_power_abs = np.sum(psds[i, idx])
                        features[f'eeg_{ch}_{band_name}_de'] = self._calc_differential_entropy(band_power_abs, eps)

                features['eeg_ch1_sampen'] = sample_entropy(data_filt[0])
                features['eeg_ch2_sampen'] = sample_entropy(data_filt[1])
                features['eeg_ch1_permen'] = permutation_entropy(data_filt[0])
                features['eeg_ch2_permen'] = permutation_entropy(data_filt[1])

                for band in ['alpha', 'theta']:
                    left = features.get(f'eeg_ch1_{band}', eps)
                    right = features.get(f'eeg_ch2_{band}', eps)
                    features[f'eeg_asym_{band}'] = np.log(right + eps) - np.log(left + eps)

                for ch in ['ch1', 'ch2']:
                    beta = features.get(f'eeg_{ch}_beta', eps)
                    alpha = features.get(f'eeg_{ch}_alpha', eps)
                    features[f'eeg_{ch}_beta_alpha_ratio'] = beta / alpha
                features['eeg_beta_alpha_ratio_avg'] = (features['eeg_ch1_beta_alpha_ratio'] + features['eeg_ch2_beta_alpha_ratio']) / 2

                for ch in ['ch1', 'ch2']:
                    theta = features.get(f'eeg_{ch}_theta', eps)
                    beta = features.get(f'eeg_{ch}_beta', eps)
                    features[f'eeg_{ch}_theta_beta_ratio'] = theta / beta
                features['eeg_theta_beta_ratio_avg'] = (features['eeg_ch1_theta_beta_ratio'] + features['eeg_ch2_theta_beta_ratio']) / 2

                features['eeg_sampen_asym'] = features['eeg_ch2_sampen'] - features['eeg_ch1_sampen']
                features['eeg_permen_asym'] = features['eeg_ch2_permen'] - features['eeg_ch1_permen']

            except Exception as e:
                logger.warning(f"EEG特征提取失败，跳过EEG模态: {e}")
        eeg_time = time_module.time() - start_eeg

        # ========== PPG 特征（含LF/HF计算）==========
        start_ppg = time_module.time()
        hr_mean = 0.0
        ppg_features_success = False
        
        if ppg_valid:
            try:
                # 仅做基础清理（去除无穷值、插值）
                ppg_clean = np.array(ppg, dtype=np.float64).flatten()
                if not np.all(np.isfinite(ppg_clean)):
                    mask = np.isfinite(ppg_clean)
                    if np.any(mask):
                        x_valid = np.where(mask)[0]
                        x_all = np.arange(len(ppg_clean))
                        ppg_clean = np.interp(x_all, x_valid, ppg_clean[mask])
                    else:
                        ppg_clean = np.zeros_like(ppg_clean)
                
                if np.std(ppg_clean) < 1e-6:
                    raise ValueError("Flat PPG signal")
                
                # 直接传入原始数组，不再做归一化
                ppg_features, hr_mean, ppg_features_success = self._compute_ppg_features_safe(ppg_clean)
                
                if ppg_features_success and ppg_features is not None:
                    features.update(ppg_features)
                    logger.info(f"PPG特征提取成功: HR={hr_mean:.1f}, RMSSD={ppg_features.get('hrv_rmssd', 0):.1f}")
                else:
                    logger.warning("PPG特征提取失败，尝试备用方案")
                    # 可保留原有备用方案作为 fallback
                    ppg_features, hr_mean, ppg_features_success = self._compute_ppg_features_fallback(ppg_clean)
                    if ppg_features_success:
                        features.update(ppg_features)
                    else:
                        logger.warning("备用PPG方案也失败，跳过PPG模态")
                        ppg_valid = False
                        
            except Exception as e:
                logger.warning(f"PPG处理异常，跳过PPG模态: {e}")
                ppg_valid = False

            # 新增BF/FHF特征（仅当PPG有效且心率合理）
            if ppg_valid and hr_mean > 30 and hr_mean < 200 and len(ppg) >= self.fs_ppg * 10:
                bf_power, fhf_power, bf_fhf_ratio = self._calc_bf_fhf(ppg, hr_mean, eps)
                features['ppg_bf_power'] = bf_power
                features['ppg_fhf_power'] = fhf_power
                features['ppg_bf_fhf_ratio'] = bf_fhf_ratio
            elif ppg_valid:
                features['ppg_bf_power'] = 0.0
                features['ppg_fhf_power'] = 0.0
                features['ppg_bf_fhf_ratio'] = 0.0

        ppg_time = time_module.time() - start_ppg

        # ========== GSR 特征 ==========
        start_gsr = time_module.time()
        if gsr_valid:
            try:
                gsr_array = np.array(gsr, dtype=np.float64).flatten()
                gsr_array = np.clip(gsr_array, -10000, 10000)
                if not np.all(np.isfinite(gsr_array)):
                    mask = np.isfinite(gsr_array)
                    if np.any(mask):
                        x_valid = np.where(mask)[0]
                        x_all = np.arange(len(gsr_array))
                        gsr_array = np.interp(x_all, x_valid, gsr_array[mask])
                    else:
                        gsr_array = np.zeros_like(gsr_array)

                decomposed = nk.eda_phasic(gsr_array, sampling_rate=self.fs_gsr, method='cvxeda')
                phasic = decomposed['EDA_Phasic'].values
                tonic = decomposed['EDA_Tonic'].values

                tonic_mean = np.mean(tonic)
                if tonic_mean > 0:
                    features['gsr_scl_mean'] = float(tonic_mean)
                else:
                    features['gsr_scl_mean'] = float(np.mean(gsr_array))

                if len(gsr_array) > 1:
                    x = np.arange(len(gsr_array))
                    slope = np.polyfit(x, gsr_array, 1)[0]
                    features['gsr_scl_slope'] = float(slope * self.fs_gsr)
                else:
                    features['gsr_scl_slope'] = 0.0

                scr_peaks = []
                methods_tried = []
                try:
                    peaks_info = nk.eda_findpeaks(phasic, sampling_rate=self.fs_gsr, method='gamboa2008', amplitude_min=0.01)
                    scr_peaks = peaks_info['SCR_Peaks']
                    methods_tried.append(f"gamboa2008_0.01({len(scr_peaks)})")
                except Exception:
                    methods_tried.append(f"gamboa2008_0.01(fail)")

                if len(scr_peaks) == 0:
                    try:
                        peaks_info = nk.eda_findpeaks(phasic, sampling_rate=self.fs_gsr, method='kim2004', amplitude_min=0.01)
                        scr_peaks = peaks_info['SCR_Peaks']
                        methods_tried.append(f"kim2004_0.01({len(scr_peaks)})")
                    except Exception:
                        methods_tried.append(f"kim2004_0.01(fail)")

                if len(scr_peaks) == 0:
                    try:
                        peaks_info = nk.eda_findpeaks(phasic, sampling_rate=self.fs_gsr, method='neurokit')
                        scr_peaks = peaks_info['SCR_Peaks']
                        methods_tried.append(f"neurokit({len(scr_peaks)})")
                    except Exception:
                        methods_tried.append(f"neurokit(fail)")

                if len(scr_peaks) == 0:
                    try:
                        from scipy.signal import savgol_filter
                        phasic_smooth = savgol_filter(phasic, window_length=7, polyorder=2)
                        peaks, _ = find_peaks(phasic_smooth, height=np.std(phasic_smooth)*0.3, distance=self.fs_gsr//2)
                        scr_peaks = peaks
                        methods_tried.append(f"scipy({len(scr_peaks)})")
                    except Exception:
                        methods_tried.append(f"scipy(fail)")

                logger.debug(f"GSR方法尝试: {', '.join(methods_tried)}")

                if len(scr_peaks) > 0:
                    amplitudes = phasic[scr_peaks]
                    amplitudes = amplitudes[amplitudes > 0]
                    features['gsr_scr_count'] = int(len(amplitudes))
                    features['gsr_scr_amplitude_mean'] = float(np.mean(amplitudes)) if len(amplitudes) > 0 else 0.0
                    features['gsr_scr_amplitude_max'] = float(np.max(amplitudes)) if len(amplitudes) > 0 else 0.0
                    features['gsr_scr_auc'] = float(np.trapz(phasic) / self.fs_gsr)
                else:
                    features['gsr_scr_count'] = 0
                    features['gsr_scr_amplitude_mean'] = 0.0
                    features['gsr_scr_amplitude_max'] = 0.0
                    features['gsr_scr_auc'] = float(np.trapz(phasic) / self.fs_gsr)

                if features['gsr_scl_mean'] > 1e-12:
                    features['gsr_scr_amplitude_scl_ratio'] = features['gsr_scr_amplitude_mean'] / features['gsr_scl_mean']
                else:
                    features['gsr_scr_amplitude_scl_ratio'] = 0.0

            except Exception as e:
                logger.warning(f"GSR特征提取失败，跳过GSR模态: {e}")

        gsr_time = time_module.time() - start_gsr

        total_time = time_module.time() - start_total
        logger.info(f"特征提取耗时: EEG={eeg_time:.2f}s, PPG={ppg_time:.2f}s, GSR={gsr_time:.2f}s, 总计={total_time:.2f}s")
        return features

# ==================== PAD计算函数（完整版） ====================
def pad_from_features(features):
    # 缩放因子（基于最新统计调整）
    scale = {
        'eeg_asym_alpha': 5.0,
        'eeg_asym_theta': 5.1,
        'eeg_beta_alpha_ratio_avg': 230,
        'eeg_theta_beta_ratio_avg': 3.1,
        'eeg_sampen_asym': 0.6,
        'hrv_rmssd': 50.0,
        'hrv_sdnn': 100.0,
        'hr_mean': 90.0,
        'hrv_sd1_sd2': 0.6,
        'gsr_scl_mean': 335.0,
        'gsr_scl_slope': 0.27,
        'gsr_scr_count': 50.0,
        'gsr_scr_auc': 2000000.0,
        'gsr_scr_amplitude_scl_ratio': 110.0,
        'eeg_ch1_alpha_de': 5.0,
        'eeg_ch2_alpha_de': 4.7,
        'eeg_ch1_beta_de': 4.1,
        'eeg_ch2_beta_de': 1.7,
        'ppg_bf_power': 15000.0,
        'ppg_fhf_power': 4500.0,
        'ppg_bf_fhf_ratio': 7.0,
        'hrv_hf': 1000.0,
        'hrv_lf_hf': 15.0,
    }

    weights = {
        'P': {
            'eeg_asym_alpha': 0.5,
            'hrv_rmssd': 0.3,
            'eeg_ch1_alpha_de': 0.2,
            'eeg_ch2_alpha_de': 0.2,
            'eeg_ch1_beta_de': -0.1,
            'eeg_ch2_beta_de': -0.1,
            'ppg_bf_power': 0.2,
            'ppg_fhf_power': -0.1,
            'ppg_bf_fhf_ratio': 0.2,
            'hrv_hf': 0.2,
        },
        'A': {
            'gsr_scl_mean': 0.2,
            'gsr_scr_count': 0.3,
            'gsr_scl_slope': 0.2,
            'gsr_scr_auc': 0.1,
            'hrv_sdnn': 0.2,
            'hrv_rmssd': -0.2,
            'hr_mean': 0.3,
            'hrv_lf_hf': 0.2,                        # 新增
        },
        'D': {
            'eeg_asym_theta': 0.2,
            'eeg_beta_alpha_ratio_avg': 0.2,
            'eeg_theta_beta_ratio_avg': -0.2,
            'eeg_sampen_asym': 0.15,
            'hrv_rmssd': 0.15,
            'hrv_sdnn': 0.1,
            'hrv_sd1_sd2': 0.2,
            'gsr_scr_amplitude_scl_ratio': 0.15,
        }
    }

    pad = {}
    for dim, wdict in weights.items():
        val = 0.0
        total_weight = 0.0
        for feat, w in wdict.items():
            if feat in features:
                raw = features[feat]
                if np.isfinite(raw):
                    s = scale.get(feat, 1.0)
                    val += w * (raw / s)
                    total_weight += abs(w)
                else:
                    logger.warning(f"特征 {feat} 值为 {raw}，跳过")
            else:
                logger.debug(f"特征 {feat} 缺失，跳过")
        if total_weight > 0:
            pad[dim] = np.clip(val / total_weight, -1.0, 1.0)
            logger.debug(f"dim {dim}: val={val:.3f}, total_weight={total_weight:.3f}, result={pad[dim]:.3f}")
        else:
            pad[dim] = 0.0
            logger.debug(f"dim {dim}: total_weight=0，设为0")
    return pad

# ==================== 离屏截图生成函数（基于原PADCubeVisualizer） ====================
def generate_snapshot(history_points):
    """根据历史点生成情绪立方体截图（离屏渲染）"""
    pv.global_theme.allow_empty_mesh = True
    plotter = pv.Plotter(window_size=[900, 700], off_screen=True)
    plotter.set_background('white')
    plotter.enable_anti_aliasing()

    # 绘制立方体
    cube = pv.Cube(center=(0,0,0), x_length=2, y_length=2, z_length=2)
    plotter.add_mesh(cube, color='lightblue', opacity=0.1, smooth_shading=True)
    plotter.add_mesh(cube, style='wireframe', color='gray', line_width=1, opacity=0.6)

    # 原点标记
    origin = pv.Sphere(center=(0,0,0), radius=0.02)
    plotter.add_mesh(origin, color='gold', smooth_shading=True)

    # 基准情绪点（来自原文件）
    base_emotions = [
        ("Angry", -0.7, 0.8, 0.3, 'red'),
        ("Disgust", -0.6, 0.4, 0.6, 'darkgray'),
        ("Fear", -0.8, 0.8, -0.5, 'purple'),
        ("Happiness", 0.8, 0.4, 0.2, 'green'),
        ("Calm", 0.1, -0.8, 0.1, 'lightblue'),
        ("Sadness", -0.8, -0.2, -0.6, 'blue'),
        ("Surprise", 0.4, 0.7, -0.15, 'orange'),
        ("Anxiety", -0.5, 0.6, -0.5, 'black'),
        ("Stress", -0.4, 0.7, -0.4, 'yellow'),
    ]
    for name, px, ay, dz, color in base_emotions:
        sphere = pv.Sphere(center=(px, ay, dz), radius=0.04)
        plotter.add_mesh(sphere, color=color, opacity=1.0, smooth_shading=True)
        plotter.add_point_labels([(px+0.1, ay+0.1, dz+0.1)], [name],
                                 text_color='black', font_size=12,
                                 point_size=0, show_points=False)

    # 历史点云（用户情绪轨迹）
    if len(history_points) > 0:
        points = np.array(history_points)
        cloud = pv.PolyData(points)
        time_vals = np.linspace(0, 1, len(points))
        cloud.point_data['time'] = time_vals
        plotter.add_mesh(cloud, render_points_as_spheres=True, point_size=10,
                         scalars='time', cmap='plasma', opacity='linear', show_scalar_bar=False)

    # 当前情绪点（绿色大球）
    if len(history_points) > 0:
        current = history_points[-1]
        curr_sphere = pv.Sphere(center=current, radius=0.05)
        plotter.add_mesh(curr_sphere, color='green', smooth_shading=True)

    # 坐标轴标签
    label_offset = 1.4
    plotter.add_point_labels([(label_offset, 0, 0)], ["Pleasure"],
                             text_color='red', font_size=20, point_size=0, show_points=False)
    plotter.add_point_labels([(0, label_offset, 0)], ["Arousal"],
                             text_color='green', font_size=20, point_size=0, show_points=False)
    plotter.add_point_labels([(0, 0, label_offset)], ["Dominance"],
                             text_color='blue', font_size=20, point_size=0, show_points=False)

    plotter.show_grid(color='lightgray')
    plotter.show_axes()
    plotter.camera_position = 'iso'

    # 截图并返回 PIL Image
    img = plotter.screenshot(return_img=True)
    plotter.close()
    return Image.fromarray(img)

# ==================== 多模态引擎类 ====================
class MultiModalEngine:
    def __init__(self,
                 serial_port='/dev/ttyACM0', baudrate=115200,
                 fs_eeg=256, fs_ppg=125, fs_gsr=100,
                 eeg_window_sec=2, ppg_gsr_window_sec=60, hop_sec=2,
                 history_length=120):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.fs_eeg = fs_eeg
        self.fs_ppg = fs_ppg
        self.fs_gsr = fs_gsr
        self.eeg_window_sec = eeg_window_sec
        self.ppg_gsr_window_sec = ppg_gsr_window_sec
        self.hop_sec = hop_sec
        self.history_length = history_length
        self.modality_valid = {'eeg': False, 'ppg': False, 'gsr': False}

        # 数据缓冲区（线程安全，需加锁）
        self.eeg_buffer = deque()          # (timestamp, ch1, ch2)
        self.ppg_buffer = deque()          # (timestamp, value)
        self.gsr_buffer = deque()          # (timestamp, value)
        self.lock = threading.Lock()

        # 当前PAD和历史
        self.current_pad = {'P': 0.0, 'A': 0.0, 'D': 0.0}
        self.history = deque(maxlen=history_length)

        # 特征提取器
        self.extractor = MultimodalFeatureExtractor(fs_eeg, fs_ppg, fs_gsr, use_wavelet=False)

        # EEG连接相关
        self.last_eeg_address_file = os.path.expanduser("~/.emopad_last_eeg.txt")
        self.last_eeg_address = self._load_last_eeg_address()

        # 运行标志
        self.running = False
        self.ble_task = None
        self.serial_reader = None
        
        self.base_emotions = [
            ("Angry", -0.7, 0.8, 0.3),
            ("Disgust", -0.6, 0.4, 0.6),
            ("Fear", -0.8, 0.8, -0.5),
            ("Happiness", 0.8, 0.4, 0.2),
            ("Calm", 0.1, -0.8, 0.1),
            ("Sadness", -0.8, -0.2, -0.6),
            ("Surprise", 0.4, 0.7, -0.15),
            ("Anxiety", -0.5, 0.6, -0.5),
            ("Stress", -0.4, 0.7, -0.4)
        ]

    def get_closest_emotion(self, pad):
        min_dist_sq = float('inf')
        closest_name = None
        px, ay, dz = pad['P'], pad['A'], pad['D']
        for name, ex, ey, ez in self.base_emotions:
            dx = px - ex
            dy = ay - ey
            dz_ = dz - ez
            dist_sq = dx*dx + dy*dy + dz_*dz_
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_name = name
        distance = np.sqrt(min_dist_sq)
        return closest_name, distance

    def _load_last_eeg_address(self):
        if os.path.exists(self.last_eeg_address_file):
            with open(self.last_eeg_address_file, 'r') as f:
                addr = f.read().strip()
                if addr:
                    return addr
        return None

    def _save_last_eeg_address(self, address):
        with open(self.last_eeg_address_file, 'w') as f:
            f.write(address)

    # ---------- 数据馈送（线程安全） ----------
    def feed_eeg(self, timestamp, ch1, ch2):
        with self.lock:
            self.eeg_buffer.append((timestamp, ch1, ch2))
            # 限制缓冲区长度（约30秒数据）
            max_len = int(70 * self.fs_eeg)
            if len(self.eeg_buffer) > max_len:
                self.eeg_buffer.popleft()

    def feed_ppg_gsr(self, timestamp, ppg, gsr):
        with self.lock:
            self.ppg_buffer.append((timestamp, ppg))
            self.gsr_buffer.append((timestamp, gsr))
            max_len = int(70 * max(self.fs_ppg, self.fs_gsr))
            if len(self.ppg_buffer) > max_len:
                self.ppg_buffer.popleft()
                self.gsr_buffer.popleft()

    # ---------- BLE EEG 连接与数据采集 ----------
    async def find_and_connect_eeg(self):
        if self.last_eeg_address:
            logger.info(f"尝试连接上次使用的设备: {self.last_eeg_address}")
            client = BleakClient(self.last_eeg_address)
            try:
                await client.connect(timeout=30.0)
                if client.is_connected:
                    logger.info("连接成功")
                    return client
                else:
                    logger.info("连接失败，将进行扫描")
            except Exception as e:
                logger.error(f"连接上次设备失败: {e}")

        logger.info("扫描BLE EEG设备...")
        devices = await BleakScanner.discover(timeout=30.0)
        eeg_device = None
        for d in devices:
            if d.name and 'KSEEG' in d.name.upper():
                eeg_device = d
                break

        if not eeg_device:
            raise RuntimeError("未找到KSEEG102设备")

        logger.info(f"找到设备: {eeg_device.name} ({eeg_device.address})")
        client = BleakClient(eeg_device.address)
        await client.connect(timeout=30.0)
        if not client.is_connected:
            raise RuntimeError("连接失败")
        logger.info("BLE连接成功")

        self._save_last_eeg_address(eeg_device.address)
        self.last_eeg_address = eeg_device.address
        return client

    async def run_ble(self):
        while self.running:
            client = None
            handler = None
            try:
                # 1. 连接设备
                client = await self.find_and_connect_eeg()
                # 2. 创建处理器并启动
                handler = KSEEG102Handler(client, self._eeg_callback)
                await handler.start()
                # 3. 等待连接断开或停止信号
                while self.running and client.is_connected:
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"BLE连接异常: {e}")
            finally:
                # 4. 确保清理旧连接
                if handler:
                    try:
                        await handler.stop()
                    except Exception as e:
                        logger.warning(f"停止处理器时出错: {e}")
                if client and client.is_connected:
                    try:
                        await client.disconnect()
                    except Exception as e:
                        logger.warning(f"断开连接时出错: {e}")
                # 5. 如果仍在运行，等待后重连
                if self.running:
                    logger.warning("BLE连接已断开，5秒后尝试重连...")
                    await asyncio.sleep(5)
    def _eeg_callback(self, timestamp, ch1, ch2):
        # 直接调用 feed_eeg 更新 eeg_buffer
        self.feed_eeg(timestamp, ch1, ch2)
        logger.info(f"EEG callback: ts={timestamp:.3f}, ch1={ch1:.2f}, ch2={ch2:.2f}")

    # ---------- 窗口处理循环 ----------
    async def process_windows(self):
        await asyncio.sleep(max(self.eeg_window_sec, self.ppg_gsr_window_sec))  # 等待缓冲区预热
        while self.running:
            try:
                await self._process_one_window()
            except Exception as e:
                logger.error(f"窗口处理异常: {e}")
            await asyncio.sleep(self.hop_sec)

    async def _process_one_window(self):
        # 获取当前时间窗口内的数据（需要复制缓冲区，避免长时间持锁）
        t_end = time.time()
        t_start_eeg = t_end - self.eeg_window_sec
        t_start_ppg_gsr = t_end - self.ppg_gsr_window_sec

        with self.lock:
            eeg_data = [(ts, ch1, ch2) for ts, ch1, ch2 in self.eeg_buffer if t_start_eeg <= ts <= t_end]
            ppg_data = [(ts, val) for ts, val in self.ppg_buffer if t_start_ppg_gsr <= ts <= t_end]
            gsr_data = [(ts, val) for ts, val in self.gsr_buffer if t_start_ppg_gsr <= ts <= t_end]

        logger.info(f"窗口数据量: eeg={len(eeg_data)} (need {self.fs_eeg * 1.5}), ppg={len(ppg_data)}, gsr={len(gsr_data)}")

        if len(eeg_data) < self.fs_eeg * 1.5:
            logger.info("窗口内EEG数据不足，将仅使用PPG/GSR（如果可用）")
        if len(ppg_data) < self.fs_ppg * 2:
            logger.info("窗口内PPG数据不足，将仅使用EEG/GSR（如果可用）")
        if len(gsr_data) < self.fs_gsr * 2:
            logger.info("窗口内GSR数据不足，将仅使用EEG/PPG（如果可用）")

        # 排序（其实时间戳基本有序，但保险）
        eeg_sorted = sorted(eeg_data, key=lambda x: x[0])
        ppg_sorted = sorted(ppg_data, key=lambda x: x[0])
        gsr_sorted = sorted(gsr_data, key=lambda x: x[0])

        eeg_ch1 = np.array([v for _, v, _ in eeg_sorted])
        eeg_ch2 = np.array([v for _, _, v in eeg_sorted])
        ppg = np.array([v for _, v in ppg_sorted])
        gsr = np.array([v for _, v in gsr_sorted])

        # 特征提取（耗时操作，放在线程中执行）
        try:
            features = await asyncio.to_thread(
                self.extractor.extract,
                eeg_ch1, eeg_ch2, ppg, gsr
            )
        except Exception as e:
            logger.error(f"特征提取失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return

        # 计算PAD
        pad = pad_from_features(features)
        logger.info(f"计算得到的PAD: P={pad['P']:.3f}, A={pad['A']:.3f}, D={pad['D']:.3f}")
        
        modality_valid = {
        'eeg': any(key.startswith('eeg_') for key in features.keys()),
        'ppg': any(key.startswith('hr_') or key.startswith('hrv_') for key in features.keys()),
        'gsr': any(key.startswith('gsr_') for key in features.keys()),
        }
    
        # 更新引擎状态（加锁）
        with self.lock:
            self.current_pad = pad
            self.history.append((pad['P'], pad['A'], pad['D']))
            self.modality_valid = modality_valid


    # ---------- 启动/停止 ----------
    async def start(self):
        self.running = True
        # 启动串口读取线程
        self.serial_reader = SerialReader(self.serial_port, self.baudrate, self.feed_ppg_gsr)
        self.serial_reader.start()
        # 启动BLE任务
        self.ble_task = asyncio.create_task(self.run_ble())
        # 启动窗口处理任务
        self.window_task = asyncio.create_task(self.process_windows())
        logger.info("多模态引擎已启动")

    async def stop(self):
        self.running = False
        if self.serial_reader:
            self.serial_reader.stop()
        if self.ble_task:
            self.ble_task.cancel()
            try:
                await self.ble_task
            except asyncio.CancelledError:
                pass
        if hasattr(self, 'window_task'):
            self.window_task.cancel()
            try:
                await self.window_task
            except asyncio.CancelledError:
                pass
        logger.info("多模态引擎已停止")

    # ---------- API 数据获取 ----------
    def get_current_pad(self):
        with self.lock:
            return self.current_pad.copy()

    def get_history(self, n=None):
        with self.lock:
            if n is None:
                return list(self.history)
            return list(self.history)[-n:]

# ==================== FastAPI 应用 ====================
app = FastAPI(title="多模态情绪PAD服务", description="实时计算Pleasure-Arousal-Dominance并提供情绪立方体截图")

# 全局引擎实例（在启动时初始化）
engine = None

def find_serial_port():
    """自动检测可用的串口设备"""
    import glob
    # 尝试常见的串口设备
    candidates = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyUSB0', '/dev/ttyUSB1']
    
    for port in candidates:
        if os.path.exists(port):
            logger.info(f"找到串口设备: {port}")
            return port
    
    # 如果没有找到，使用默认的
    logger.warning("未找到串口设备，使用默认 /dev/ttyACM0")
    return '/dev/ttyACM0'

@app.on_event("startup")
async def startup_event():
    global engine
    # 自动检测串口
    SERIAL_PORT = find_serial_port()
    BAUDRATE = 115200
    engine = MultiModalEngine(
        serial_port=SERIAL_PORT,
        baudrate=BAUDRATE,
        eeg_window_sec=2,
        ppg_gsr_window_sec=60,
        hop_sec=2,
        history_length=120
    )
    await engine.start()
    logger.info(f"FastAPI 启动完成，引擎已运行 (串口: {SERIAL_PORT})")

@app.on_event("shutdown")
async def shutdown_event():
    if engine:
        await engine.stop()

@app.get("/pad")
async def get_pad():
    if engine is None:
        return JSONResponse(status_code=503, content={"error": "引擎未初始化"})
    pad = engine.get_current_pad()
    # 新增：获取模态有效性（需加锁读取）
    with engine.lock:
        valid = engine.modality_valid.copy()
    closest, dist = engine.get_closest_emotion(pad)
    return JSONResponse(content={
        "P": pad["P"],
        "A": pad["A"],
        "D": pad["D"],
        "closest_emotion": closest,
        "distance": dist,
        "eeg_valid": valid["eeg"],
        "ppg_valid": valid["ppg"],
        "gsr_valid": valid["gsr"]
    })

@app.get("/history")
async def get_history(n: int = 120):
    """获取最近 n 个历史点（默认120个）"""
    if engine is None:
        return JSONResponse(status_code=503, content={"error": "引擎未初始化"})
    points = engine.get_history(n)
    return JSONResponse(content={"points": points})

@app.get("/snapshot")
async def snapshot():
    """生成当前情绪立方体截图（PNG）"""
    if engine is None:
        return Response(content="引擎未初始化", status_code=503)
    history = engine.get_history(120)
    if not history:
        return Response(content="尚无足够历史数据", status_code=503)
    try:
        img = generate_snapshot(history)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        logger.error(f"截图生成失败: {e}")
        return Response(content="截图生成失败", status_code=500)

if __name__ == "__main__":
    # 启动 uvicorn 服务
    uvicorn.run(app, host="127.0.0.1", port=8766, log_level="info")