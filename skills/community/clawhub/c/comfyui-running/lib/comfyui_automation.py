#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ComfyUI 全自动运行模块 - 跨平台兼容版
=====================================

【功能概述】
    1. 自动检测/启动 ComfyUI (Windows / Linux / macOS / WSL)
    2. 自动选择工作流
    3. 执行工作流
    4. 返回生成结果

【支持平台】
    - Windows: ComfyUI-aki-v3 (秋叶版), 官方版
    - Linux: 官方版 ComfyUI
    - macOS: 官方版 ComfyUI
    - WSL: 访问 Windows 版或 Linux 版

【Windows vs Linux 关键差异】

    | 差异项       | Windows                    | Linux/macOS              |
    |-------------|---------------------------|-------------------------|
    | Python 路径  | python.exe                | python3                 |
    | 启动脚本     | python.bat / run.bat      | python.sh               |
    | 路径格式     | H:/ComfyUI 或 H:\\ComfyUI | /opt/ComfyUI            |
    | WSL 路径    | /mnt/h/ComfyUI            | -                       |
    | 进程启动     | subprocess.Popen (Windows) | start_new_session=True  |
    | 浏览器路径   | C:\\Program Files\\...     | /usr/bin/...            |

【常见问题】
    1. 'int' object is not subscriptable
       → 节点链接必须用 ["node_id", slot] 格式，不能用整数

    2. 启动失败
       → 检查 config.json 中 comfyui_root 和 python_path 是否正确

    3. 路径问题
       → 始终使用正斜杠 / 或 os.path.join()，避免硬编码反斜杠
"""
import os
import sys
import json
import time
import socket
import subprocess
import requests
import platform
import shutil
from typing import Optional, Dict, List, Tuple, Union

# ============ 导入配置模块 ============
# 兼容两种导入方式：
# 1. 作为包导入: from .comfyui_config import ...
# 2. 直接运行: from comfyui_config import ...
try:
    from .comfyui_config import (
        get_comfyui_root,
        get_comfyui_port,
        get_workflows_dir,
        get_output_dir,
        get_python_path,
        get_browser_path,
        get_browser_type,
        get_ui_type,
        _get_system,
        _is_wsl,
    )
except ImportError:
    from comfyui_config import (
        get_comfyui_root,
        get_comfyui_port,
        get_workflows_dir,
        get_output_dir,
        get_python_path,
        get_browser_path,
        get_browser_type,
        get_ui_type,
        _get_system,
        _is_wsl,
    )


class ComfyUIAutomation:
    """
    ComfyUI 全自动运行类（跨平台版）
    
    【初始化流程】
        1. 读取配置（config.json / 环境变量 / 自动检测）
        2. 检测 ComfyUI 是否运行
        3. 优先使用 skill 内置的 example_workflows
    
    【跨平台兼容】
        - Windows: 支持秋叶版和官方版
        - Linux: 支持官方版
        - WSL: 自动检测访问 Windows 或 Linux 安装
    """
    
    def __init__(self):
        # ========== 配置读取 ==========
        self.comfyui_root = get_comfyui_root()
        self.port = get_comfyui_port()
        self.python_path = get_python_path()
        self.output_dir = get_output_dir()
        self.ui_type = get_ui_type()
        self.browser_path = get_browser_path()
        self.browser_type = get_browser_type()
        
        # 优先使用 skill 自带的 example_workflows 目录
        # 这样用户解压后无需配置即可使用
        skill_wf_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "..", 
            "example_workflows"
        )
        skill_wf_dir = os.path.normpath(skill_wf_dir)
        if os.path.isdir(skill_wf_dir):
            self.workflows_dir = skill_wf_dir
        else:
            self.workflows_dir = get_workflows_dir()
        
        self.base_url = f"http://127.0.0.1:{self.port}"
        self.process = None
        self.browser_process = None
        
        # 自动检测 UI 类型
        if self.ui_type == "auto":
            self.ui_type = self._detect_ui_type()
    
    def _detect_ui_type(self):
        """
        自动检测 ComfyUI UI 类型
        
        【检测规则】
            1. 路径包含 "aki"、"秋叶"、"v3" → aki
            2. 存在 extra_model_paths.yaml → aki（秋叶版特征文件）
            3. 其他 → official
        
        【返回值】
            "aki" 或 "official"
        """
        if not self.comfyui_root:
            return "official"
        
        # 秋叶版特征
        aki_markers = ["aki", "秋叶", "v3", "v1.4"]
        root_lower = self.comfyui_root.lower()
        for marker in aki_markers:
            if marker in root_lower:
                return "aki"
        
        # 检查秋叶版特征文件
        if os.path.exists(os.path.join(self.comfyui_root, "extra_model_paths.yaml")):
            return "aki"
        
        return "official"
    
    def _get_python_executable(self):
        """
        获取 Python 可执行命令
        
        【Windows vs Linux 差异】
            Windows: 返回 python.exe 或配置中的路径
            Linux:   返回 python3
        
        【返回值】
            Python 命令字符串
        """
        system = _get_system()
        
        if system == "windows":
            # Windows: 优先使用配置的 python_path
            return self.python_path if self.python_path else "python.exe"
        else:
            # Linux/macOS: 使用 python3
            return self.python_path if self.python_path else "python3"
    
    def is_comfyui_running(self) -> bool:
        """
        检测 ComfyUI 是否正在运行
        
        【检测方法】
            GET http://127.0.0.1:{port}/system_stats
            返回 200 表示正在运行
        
        【返回值】
            True  - 正在运行
            False - 未运行
        """
        try:
            r = requests.get(f"{self.base_url}/system_stats", timeout=2)
            return r.status_code == 200
        except Exception:
            return False
    
    def wait_for_comfyui(self, timeout: int = 60) -> bool:
        """
        等待 ComfyUI 启动
        
        【参数】
            timeout - 超时时间（秒）
        
        【返回值】
            True  - 启动成功
            False - 超时
        """
        for i in range(timeout):
            if self.is_comfyui_running():
                return True
            time.sleep(1)
        return False
    
    def _clean_env(self):
        """
        清理可能干扰的环境变量
        
        【清理内容】
            - 代理相关环境变量 (HTTP_PROXY, HTTPS_PROXY, ALL_PROXY)
            - 防止代理设置导致本地连接失败
        
        【注意】
            仅清理当前进程的环境变量，不影响系统设置
        """
        for k in list(os.environ.keys()):
            if 'proxy' in k.lower() or k.upper() in ('HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY'):
                del os.environ[k]
    
    def _build_start_command(self):
        """
        构建启动命令（跨平台）
        
        【Windows 命令】
            python.exe main.py --listen 0.0.0.0 --port 8188
        
        【Linux 命令】
            python3 main.py --listen 0.0.0.0 --port 8188
        
        【返回值】
            (command_list, error_message)
            - command_list: 启动命令列表 或 None
            - error_message: 错误信息 或 None
        """
        if not self.comfyui_root:
            return None, "comfyui_root not configured"
        
        main_py = os.path.join(self.comfyui_root, "main.py")
        if not os.path.exists(main_py):
            return None, f"main.py not found: {main_py}"
        
        python_exe = self._get_python_executable()
        
        # 验证 Python 存在
        if not os.path.exists(python_exe) and python_exe not in ("python", "python3", "python.exe"):
            python_exe = "python3" if _get_system() != "windows" else "python"
        
        cmd = [
            python_exe,
            main_py,
            "--listen", "0.0.0.0",
            "--port", str(self.port)
        ]
        
        return cmd, None
    
    def start_comfyui(self) -> Tuple[bool, str]:
        """
        启动 ComfyUI（跨平台）
        
        【Windows 启动方式】
            1. 使用 subprocess.Popen
            2. 设置 SW_HIDE 隐藏窗口
            3. 捕获 PermissionError 并 fallback
        
        【Linux 启动方式】
            1. 使用 subprocess.Popen
            2. 设置 start_new_session=True 创建独立会话
            3. 输出重定向到 /dev/null
        
        【冷启动时间】
            首次启动可能需要 2-3 分钟（模型加载）
        
        【返回值】
            (success, message)
        """
        if self.is_comfyui_running():
            return True, "ComfyUI already running"
        
        cmd, err = self._build_start_command()
        if err:
            return False, err
        
        system = _get_system()
        
        try:
            self._clean_env()
            
            if system == "windows":
                # ========== Windows 启动 ==========
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE  # 隐藏窗口
                
                try:
                    self.process = subprocess.Popen(
                        cmd,
                        cwd=self.comfyui_root,
                        startupinfo=startupinfo,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        env=os.environ.copy()
                    )
                except PermissionError:
                    # PermissionError: 尝试使用系统 Python
                    system_python = self._find_python()
                    cmd[0] = system_python
                    self.process = subprocess.Popen(
                        cmd,
                        cwd=self.comfyui_root,
                        startupinfo=startupinfo,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        env=os.environ.copy()
                    )
            
            elif system in ("linux", "wsl", "darwin"):
                # ========== Linux/macOS 启动 ==========
                # start_new_session: 创建独立会话，关闭终端后进程继续运行
                self.process = subprocess.Popen(
                    cmd,
                    cwd=self.comfyui_root,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,  # Linux/macOS 必需
                    env=os.environ.copy()
                )
            
            # 等待启动（冷启动可能需要 2-3 分钟）
            if self.wait_for_comfyui(timeout=180):
                return True, "ComfyUI started"
            else:
                return False, "ComfyUI start timeout (cold start may take 2-3 minutes)"
        
        except Exception as e:
            return False, f"Start failed: {e}"
    
    def _find_python(self) -> str:
        """
        自动查找 Python 解释器路径
        
        【搜索顺序】
            1. conda 环境 (CONDA_DEFAULT_ENV)
            2. 虚拟环境 (VIRTUAL_ENV)
            3. shutil.which 查找
            4. 常见安装路径
        
        【Windows vs Linux 差异】
            Windows: 查找 Python{ver}/python.exe
            Linux:   查找 bin/python
        
        【返回值】
            Python 解释器路径
        """
        system = _get_system()
        
        # 1. conda 环境
        if "CONDA_DEFAULT_ENV" in os.environ:
            if system == "windows":
                conda_python = os.path.join(os.environ.get("CONDA_PREFIX", ""), "python.exe")
            else:
                conda_python = os.path.join(os.environ.get("CONDA_PREFIX", ""), "bin", "python")
            if os.path.exists(conda_python):
                return conda_python
        
        # 2. 虚拟环境
        if "VIRTUAL_ENV" in os.environ:
            if system == "windows":
                venv_python = os.path.join(os.environ.get("VIRTUAL_ENV", ""), "Scripts", "python.exe")
            else:
                venv_python = os.path.join(os.environ.get("VIRTUAL_ENV", ""), "bin", "python")
            if os.path.exists(venv_python):
                return venv_python
        
        # 3. shutil.which
        for name in ("python3", "python"):
            exe = shutil.which(name) if hasattr(shutil, 'which') else None
            if exe:
                return exe
        
        # 4. 常见路径
        if system == "windows":
            for ver in ["3.11", "3.10", "3.12", "3.9", "3.8"]:
                for path in [
                    f"C:\\Python{ver}\\python.exe",
                    f"C:\\Program Files\\Python{ver}\\python.exe",
                ]:
                    if os.path.exists(path):
                        return path
                user_path = os.path.expanduser(f"~\\AppData\\Local\\Programs\\Python\\Python{ver}\\python.exe")
                if os.path.exists(user_path):
                    return user_path
            return "python.exe"
        else:
            return "python3"
    
    def ensure_comfyui_running(self) -> Tuple[bool, str]:
        """
        确保 ComfyUI 正在运行
        
        【逻辑】
            1. 检查是否已运行
            2. 未运行则尝试启动
        
        【返回值】
            (success, message)
        """
        if self.is_comfyui_running():
            return True, "ComfyUI running"
        return self.start_comfyui()
    
    def list_workflows(self) -> List[Dict]:
        """
        列出所有可用工作流
        
        【返回值】
            工作流列表，每项包含:
            - name: 工作流名称
            - filename: 文件名
            - path: 完整路径
        """
        workflows = []
        if not self.workflows_dir or not os.path.exists(self.workflows_dir):
            return workflows
        
        for f in os.listdir(self.workflows_dir):
            if f.endswith(".json"):
                path = os.path.join(self.workflows_dir, f)
                try:
                    with open(path, "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                        workflows.append({
                            "name": f.replace(".json", ""),
                            "filename": f,
                            "path": path
                        })
                except Exception:
                    pass
        return workflows
    
    def load_workflow(self, workflow_name: str = "default") -> Optional[Dict]:
        """
        加载工作流
        
        【搜索顺序】
            1. 精确匹配 {workflow_name}.json
            2. 模糊匹配（文件名包含 workflow_name）
            3. 默认后备（default / api_format / 文生图）
        
        【支持的格式】
            - API 格式: {"node_id": {"class_type": "...", "inputs": {...}}}
            - UI 格式:  {"nodes": [...]} (自动转换)
        
        【返回值】
            工作流字典 或 None
        """
        if not self.workflows_dir:
            return None
        
        workflow_file = f"{workflow_name}.json"
        path = os.path.join(self.workflows_dir, workflow_file)
        
        if not os.path.exists(path):
            # 模糊匹配
            for f in os.listdir(self.workflows_dir):
                if f.endswith(".json") and workflow_name.lower() in f.lower():
                    path = os.path.join(self.workflows_dir, f)
                    break
        
        if not os.path.exists(path):
            # 默认后备
            for f in os.listdir(self.workflows_dir):
                if f.endswith(".json"):
                    if "default" in f.lower() or "api_format" in f.lower() or "文生图" in f:
                        path = os.path.join(self.workflows_dir, f)
                        break
        
        if not os.path.exists(path):
            return None
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except UnicodeDecodeError:
            with open(path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
        
        # UI 格式转换
        if "nodes" in data and "prompt" not in data:
            return self._convert_ui_to_api(data)
        
        return data
    
    def _convert_ui_to_api(self, ui_workflow: Dict) -> Optional[Dict]:
        """
        将 UI 格式工作流转换为 API 格式
        
        【UI 格式】
            {"nodes": [{"id": 1, "type": "CheckpointLoader", "inputs": {...}}]}
        
        【API 格式】
            {"1": {"class_type": "CheckpointLoader", "inputs": {...}}}
        
        【节点链接处理】
            ⚠️ 重要：链接上游节点时必须用 ["node_id", output_slot] 格式
            ✅ 正确: "model": ["4", 0]
            ❌ 错误: "model": 4  (会报 'int' object is not subscriptable)
        
        【返回值】
            API 格式工作流 或 None
        """
        api_workflow = {}
        nodes = ui_workflow.get("nodes", [])
        
        for node in nodes:
            node_id = str(node.get("id"))
            node_type = node.get("type")
            inputs = {}
            
            for inp in node.get("inputs", []):
                name = inp.get("name")
                if inp.get("link"):
                    continue  # 跳过链接输入（由其他节点提供）
                else:
                    if "widget" in inp:
                        inputs[name] = inp.get("default_value") or inp.get("widget", {}).get("value")
                    else:
                        inputs[name] = inp.get("default_value")
            
            # 填充默认模型（跨平台兼容）
            if node_type == "CheckpointLoaderSimple":
                inputs["ckpt_name"] = inputs.get("ckpt_name") or self._get_default_model()
            elif node_type == "EmptyLatentImage":
                inputs["width"] = inputs.get("width", 512)
                inputs["height"] = inputs.get("height", 512)
                inputs["batch_size"] = inputs.get("batch_size", 1)
            elif node_type in ("KSampler", "KSamplerAdvanced"):
                inputs["seed"] = inputs.get("seed", 0)
                inputs["steps"] = inputs.get("steps", 20)
                inputs["cfg"] = inputs.get("cfg", 8)
                inputs["sampler_name"] = inputs.get("sampler_name", "euler")
                inputs["scheduler"] = inputs.get("scheduler", "normal")
                inputs["denoise"] = inputs.get("denoise", 1)
            elif node_type == "CLIPTextEncode":
                inputs["text"] = inputs.get("text", "")
            elif node_type in ("VAEDecode", "VAEDecodeTiled"):
                # ⚠️ VAEDecode 的 samples 输入必须链接上游节点
                inputs["samples"] = inputs.get("samples", ["from", 0])
                inputs["vae"] = inputs.get("vae", ["from", 0])
            elif node_type == "SaveImage":
                # ⚠️ SaveImage 的 images 输入必须链接上游节点
                inputs["images"] = inputs.get("images", ["from", 0])
                inputs["filename_prefix"] = inputs.get("filename_prefix", "ComfyUI")
            
            if node_type:
                api_workflow[node_id] = {
                    "class_type": node_type,
                    "inputs": inputs
                }
        
        return api_workflow if api_workflow else None
    
    def _get_default_model(self):
        """获取默认模型"""
        return None  # 返回空，使用 ComfyUI 默认模型
    
    def modify_workflow_prompt(self, workflow: Dict, prompt_text: str, negative_text: str = "") -> Dict:
        """
        修改工作流提示词（智能适配不同节点结构）
        
        【参数】
            workflow     - 工作流字典
            prompt_text  - 正向提示词
            negative_text - 负向提示词
        
        【节点适配】
            自动查找 CLIPTextEncode 类型的节点：
            - 第一个给 positive（正向提示词）
            - 第二个给 negative（负向提示词）
        
        【默认值】
            如果没有提供 negative_text，使用: "low quality, worst quality, blurry"
        
        【返回值】
            修改后的工作流字典
        """
        workflow = json.loads(json.dumps(workflow))  # 深拷贝
        
        if not negative_text:
            negative_text = "low quality, worst quality, blurry, deformed, bad anatomy"
        
        # 查找所有 CLIPTextEncode 节点
        clip_nodes = []
        for node_id, node in workflow.items():
            if isinstance(node, dict) and node.get("class_type") == "CLIPTextEncode":
                clip_nodes.append(node_id)
        
        if clip_nodes:
            # 按顺序分配
            if len(clip_nodes) >= 1:
                workflow[clip_nodes[0]]["inputs"]["text"] = prompt_text
            if len(clip_nodes) >= 2:
                workflow[clip_nodes[1]]["inputs"]["text"] = negative_text
        else:
            # 传统节点 ID 回退（秋叶版常用 6, 7）
            if "6" in workflow:
                workflow["6"]["inputs"]["text"] = prompt_text
            if "7" in workflow:
                workflow["7"]["inputs"]["text"] = negative_text
        
        return workflow
    
    def queue_workflow(self, workflow: Dict, number: int = 1) -> Optional[str]:
        """
        将工作流加入队列
        
        【API 端点】
            POST http://127.0.0.1:8188/prompt
        
        【请求格式】
            {
                "prompt": {...工作流...},
                "number": 1,
                "front": true
            }
        
        【返回值】
            prompt_id 字符串 或 None
        """
        data = {
            "prompt": workflow,
            "number": number,
            "front": True
        }
        
        try:
            r = requests.post(f"{self.base_url}/prompt", json=data, timeout=10)
            if r.status_code == 200:
                return r.json().get("prompt_id")
            else:
                print(f"Queue failed: {r.status_code} {r.text}")
        except Exception as e:
            print(f"Queue failed: {e}")
        return None
    
    def get_history(self, limit: int = 5) -> Dict:
        """
        获取执行历史
        
        【API 端点】
            GET http://127.0.0.1:8188/history?per_page={limit}
        
        【返回值】
            历史记录字典
        """
        try:
            r = requests.get(f"{self.base_url}/history?per_page={limit}", timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return {}
    
    def get_latest_output(self, min_mtime: float = 0) -> Optional[str]:
        """
        获取最新生成的图片路径
        
        【策略】
            1. 从 history 获取 filename 并验证修改时间
            2. 扫描输出目录查找最新图片
        
        【参数】
            min_mtime - 最小修改时间戳（过滤旧文件）
        
        【返回值】
            图片完整路径 或 None
        """
        history = self.get_history(limit=3)
        
        # 优先使用配置的输出目录
        output_dir = self.output_dir
        if not output_dir or not os.path.isdir(output_dir):
            output_dir = os.path.join(self.comfyui_root, "output")
        
        if not os.path.isdir(output_dir):
            return None
        
        # 策略1：从 history 取 filename 并验证 mtime
        for prompt_id, data in history.items():
            if data.get("status", {}).get("completed"):
                outputs = data.get("outputs", {})
                for node_id, output in outputs.items():
                    if "images" in output:
                        images = output["images"]
                        if images:
                            filename = images[0].get("filename", "")
                            fpath = os.path.join(output_dir, filename)
                            if os.path.exists(fpath):
                                file_mtime = os.path.getmtime(fpath)
                                if file_mtime >= min_mtime - 1:
                                    return fpath
                                break
        
        # 策略2：扫描输出目录
        import glob as _glob
        pattern = os.path.join(output_dir, "*.png")
        candidates = []
        for fpath in _glob.glob(pattern):
            try:
                if os.path.getmtime(fpath) >= min_mtime - 1:
                    candidates.append((os.path.getmtime(fpath), fpath))
            except OSError:
                pass
        
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            return candidates[0][1]
        
        return None
    
    def wait_for_result(self, prompt_id: str, timeout: int = 300, submitted_at: float = 0) -> Tuple[bool, Optional[str]]:
        """
        等待工作流执行完成
        
        【轮询机制】
            每 5 秒检查一次 /history/{prompt_id}
        
        【返回值】
            (success, image_path)
            - success: True/False
            - image_path: 图片路径 或 错误信息
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            history = self.get_history(limit=10)
            
            for pid, data in history.items():
                if pid == prompt_id:
                    if data.get("status", {}).get("completed"):
                        return True, self.get_latest_output(min_mtime=submitted_at)
                    elif data.get("status", {}).get("error"):
                        error_msg = data.get("status", {}).get("error", {}).get("message", "error")
                        return False, f"Error: {error_msg}"
            
            time.sleep(5)
        
        return False, "Timeout"
    
    def generate(
        self,
        prompt: str,
        workflow_name: str = "default",
        negative: str = "",
        steps: int = 20,
        seed: Optional[int] = None,
        number: int = 1,
        batch_size: int = 1,
        width: int = 512,
        height: int = 512,
        model_name: Optional[str] = None
    ) -> Dict:
        """
        一键生成图片（核心 API）
        
        【执行流程】
            1. 检测/启动 ComfyUI
            2. 加载工作流
            3. 修改提示词
            4. 设置参数（seed, steps 等）
            5. 提交工作流
            6. 等待结果
        
        【参数】
            prompt        - 正向提示词（必填）
            workflow_name - 工作流名称（默认 "default"）
            negative      - 负向提示词（默认空）
            steps         - 采样步数（默认 20）
            seed          - 随机种子（默认随机）
            number        - 生成批次（默认 1）
            batch_size    - 每批数量（默认 1）
            width         - 图片宽度（默认 512）
            height        - 图片高度（默认 512）
            model_name    - 模型文件名（默认工作流中指定）
        
        【返回值】
            {
                "success": True/False,
                "message": "说明",
                "image_path": "图片路径",
                "prompt_id": "队列ID",
                "images": [...]
            }
        
        【示例】
            result = automation.generate("a cute cat", steps=25, seed=12345)
            if result["success"]:
                print(f"图片: {result['image_path']}")
        """
        result = {
            "success": False,
            "message": "",
            "image_path": None,
            "prompt_id": None,
            "images": []
        }
        
        # 1. 检测/启动 ComfyUI
        print("[1/5] Checking ComfyUI...")
        ok, msg = self.ensure_comfyui_running()
        if not ok:
            result["message"] = msg
            return result
        print(f"       {msg}")
        
        # 2. 加载工作流
        print(f"[2/5] Loading workflow: {workflow_name}")
        workflow = self.load_workflow(workflow_name)
        
        if not workflow:
            workflows = self.list_workflows()
            if workflows:
                workflow_name = workflows[0]["name"]
                workflow = self.load_workflow(workflow_name)
                print(f"       Auto-selected: {workflow_name}")
            else:
                result["message"] = f"No workflow found in {self.workflows_dir}"
                return result
        
        print(f"       Loaded: {workflow_name}")
        
        # 3. 设置提示词
        print(f"[3/5] Setting prompt...")
        workflow = self.modify_workflow_prompt(workflow, prompt, negative)
        
        # 4. 设置参数并提交
        if seed is None:
            seed = int(time.time() * 1000) % 10000000000
        
        # 遍历节点，应用参数
        for node_id, node in workflow.items():
            if not isinstance(node, dict):
                continue
            ctype = node.get("class_type", "")
            inputs = node.get("inputs", {})
            
            if ctype in ("KSampler", "KSamplerAdvanced"):
                inputs["steps"] = steps
                inputs["seed"] = seed
                inputs["cfg"] = inputs.get("cfg", 8)
            elif ctype == "EmptyLatentImage":
                inputs["width"] = width
                inputs["height"] = height
                inputs["batch_size"] = batch_size
            elif ctype == "CheckpointLoaderSimple":
                if model_name:
                    inputs["ckpt_name"] = model_name
        
        print(f"[4/5] Submitting (steps={steps}, seed={seed})...")
        submitted_at = time.time()
        prompt_id = self.queue_workflow(workflow, number)
        if not prompt_id:
            result["message"] = "Submit failed"
            return result
        
        result["prompt_id"] = prompt_id
        print(f"       prompt_id: {prompt_id}")
        
        # 5. 等待结果
        print(f"[5/5] Waiting for result (timeout=600s)...")
        success, output = self.wait_for_result(prompt_id, timeout=600, submitted_at=submitted_at)
        
        if success:
            result["success"] = True
            result["message"] = "Success"
            result["image_path"] = output
            print(f"       [OK] Done: {output}")
        else:
            result["message"] = output
            print(f"       [FAIL] {output}")
        
        return result


def _ensure_dependencies():
    """
    确保依赖已安装
    
    【依赖列表】
        - requests: HTTP 请求库
        - websockets: WebSocket 库（CDP 模式用）
    """
    import importlib
    for pkg, mod_name in [('requests', 'requests'), ('websockets', 'websockets')]:
        try:
            importlib.import_module(mod_name)
        except ImportError:
            print(f"[INFO] Installing dependency: {pkg}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])


def quick_generate(prompt: str, **kwargs) -> Dict:
    """
    快捷生成函数
    
    【用法】
        result = quick_generate("a cute cat")
        result = quick_generate("a landscape", steps=30, seed=42)
    
    【支持参数】
        workflow_name - 工作流名称（默认 default）
        steps         - 采样步数（默认 20）
        seed          - 随机种子（默认随机）
        negative      - 负向提示词（默认空）
        number        - 生成批次（默认 1）
        batch_size    - 每批数量（默认 1）
        width         - 图片宽度（默认 512）
        height        - 图片高度（默认 512）
        model_name    - 模型名称（可选）
    
    【返回值】
        同 generate() 方法
    """
    _ensure_dependencies()
    automation = ComfyUIAutomation()
    valid_keys = {'workflow_name', 'steps', 'seed', 'negative', 'number', 'batch_size', 'width', 'height', 'model_name'}
    filtered = {k: v for k, v in kwargs.items() if k in valid_keys}
    return automation.generate(prompt, **filtered)


# ============ 命令行入口 ============
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ComfyUI Auto Generate (Cross-Platform)")
    parser.add_argument("prompt", nargs="?", help="Prompt")
    parser.add_argument("-w", "--workflow", default="default", help="Workflow name")
    parser.add_argument("-s", "--steps", type=int, default=20, help="Steps")
    parser.add_argument("--seed", type=int, help="Seed")
    parser.add_argument("-n", "--negative", default="", help="Negative prompt")
    parser.add_argument("--batch", type=int, default=1, help="Batch size")
    
    args = parser.parse_args()
    
    if args.prompt:
        result = quick_generate(
            args.prompt,
            workflow_name=args.workflow,
            steps=args.steps,
            seed=args.seed,
            negative=args.negative,
            batch_size=args.batch
        )
        print(f"\nResult: {result['message']}")
        if result.get("image_path"):
            print(f"Image: {result['image_path']}")
    else:
        print("ComfyUI Auto Generate - usage: python comfyui_automation.py 'your prompt'")
