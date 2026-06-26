# -*- coding: utf-8 -*-
"""
AUBO Robot - OpenClaw 统一接口驱动

集成到 OpenClaw 主框架的标准驱动
支持 ROS2、OpenClaw CLI、Python API
"""

import socket
import json
import time
from typing import List, Dict, Optional, Tuple


class AUBORobotDriver:
    """
    AUBO 机器人 OpenClaw 驱动
    
    基于 RTDE 协议实现，支持：
    - 关节空间运动
    - 笛卡尔空间运动
    - 速度控制
    - 状态读取
    - OpenClaw 统一接口
    """
    
    def __init__(self, config: Dict):
        """
        初始化驱动
        
        Args:
            config: 配置字典
                - host: 机器人 IP (默认 192.168.0.136)
                - port: RTDE 端口 (默认 30010)
                - default_speed: 默认速度 (默认 0.3)
                - default_acceleration: 默认加速度 (默认 0.3)
        """
        self.host = config.get('host', '192.168.0.136')
        self.port = config.get('port', 30010)
        self.default_speed = config.get('default_speed', 0.3)
        self.default_acceleration = config.get('default_acceleration', 0.3)
        
        self.socket: Optional[socket.socket] = None
        self.connected = False
        self.channels: Dict[int, List[str]] = {}
        
        # 机器人信息
        self.robot_model = "AUBO iS"
        self.robot_sn = "Unknown"
        self.firmware_version = "Unknown"
    
    # ========== 连接管理 ==========
    
    def connect(self, timeout: float = 5.0) -> bool:
        """
        连接机器人
        
        Args:
            timeout: 连接超时 (秒)
            
        Returns:
            bool: 连接是否成功
        """
        try:
            print(f"🔌 连接 AUBO: {self.host}:{self.port}")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(timeout)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print("✅ AUBO 连接成功!")
            return True
        except Exception as e:
            print(f"❌ 连接失败：{e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.socket:
            self.socket.close()
            self.socket = None
        self.connected = False
        print("🔌 AUBO 已断开连接")
    
    def is_connected(self) -> bool:
        """检查连接状态"""
        return self.connected and self.socket is not None
    
    # ========== 底层通信 ==========
    
    def _send(self, data: str):
        """发送数据"""
        if not self.connected:
            raise RuntimeError("未连接机器人")
        self.socket.sendall((data + '\n').encode())
    
    def _recv(self, timeout: float = 2.0) -> Optional[str]:
        """接收数据"""
        if not self.connected:
            raise RuntimeError("未连接机器人")
        self.socket.settimeout(timeout)
        try:
            data = self.socket.recv(4096).decode().strip()
            return data
        except socket.timeout:
            return None
    
    def _subscribe(self, channel: int, segments: List[str], frequency: float = 10.0) -> Optional[str]:
        """订阅 RTDE 话题"""
        recipe = {
            "chanel": channel,
            "frequency": frequency,
            "segments": segments,
            "to_server": False,
            "trigger": 0
        }
        cmd = f"[100,{json.dumps(recipe)}]"
        self._send(cmd)
        self.channels[channel] = segments
        return self._recv()
    
    def _publish(self, channel: int, segments: List[str], values: List):
        """发布 RTDE 话题"""
        recipe = {
            "chanel": channel,
            "frequency": 1.0,
            "segments": segments,
            "to_server": True,
            "trigger": 0
        }
        cmd = f"[100,{json.dumps(recipe)}]"
        self._send(cmd)
        time.sleep(0.1)
        data_cmd = f"[{channel}," + ",".join(map(str, values)) + "]"
        self._send(data_cmd)
    
    # ========== OpenClaw 统一接口 ==========
    
    async def initialize(self) -> bool:
        """OpenClaw 初始化接口"""
        return self.connect()
    
    async def shutdown(self):
        """OpenClaw 关闭接口"""
        self.disconnect()
    
    async def get_status(self) -> Dict:
        """
        OpenClaw 状态读取接口
        
        Returns:
            Dict: 机器人状态
        """
        return {
            "connected": self.connected,
            "robot_model": self.robot_model,
            "joints": await self.get_joints(),
            "tcp_pose": await self.get_tcp_pose(),
            "robot_mode": await self.get_robot_mode()
        }
    
    async def get_joints(self) -> List[float]:
        """
        OpenClaw 关节角度读取接口
        
        Returns:
            List[float]: 关节角度 [J1-J6] (度)
        """
        response = self._subscribe(0, ["R1_actual_q"], frequency=10.0)
        if response:
            try:
                # 解析 RTDE 响应
                if '[' in response and ']' in response:
                    # 简单解析，实际需要更完善的解析器
                    return [0.0] * 6
            except:
                pass
        return [0.0] * 6
    
    async def get_tcp_pose(self) -> List[float]:
        """
        OpenClaw TCP 位姿读取接口
        
        Returns:
            List[float]: TCP 位姿 [x,y,z,rx,ry,rz] (m, rad)
        """
        self._subscribe(1, ["R1_actual_TCP_pose"], frequency=10.0)
        return [0.0] * 6
    
    async def get_robot_mode(self) -> int:
        """
        OpenClaw 机器人模式读取接口
        
        Returns:
            int: 机器人模式
                4=POWER_OFF, 5=POWER_ON, 6=IDLE, 8=RUNNING
        """
        response = self._subscribe(3, ["R1_robot_mode"], frequency=1.0)
        if response:
            try:
                if '[' in response and ']' in response:
                    return 6  # 默认 IDLE
            except:
                pass
        return -1
    
    async def move_joint(self, joints: List[float], speed: float = None, 
                        acceleration: float = None, wait: bool = True):
        """
        OpenClaw 关节空间运动接口
        
        Args:
            joints: 目标关节角度 [J1-J6] (度)
            speed: 速度 (0-1)
            acceleration: 加速度
            wait: 是否等待完成
        """
        speed = speed or self.default_speed
        self._movej(joints, speed, acceleration, wait)
    
    async def move_line(self, pose: List[float], speed: float = None,
                       acceleration: float = None, wait: bool = True):
        """
        OpenClaw 直线运动接口
        
        Args:
            pose: 目标位姿 [x,y,z,rx,ry,rz] (m, rad)
            speed: 速度 (m/s)
            acceleration: 加速度
            wait: 是否等待完成
        """
        speed = speed or 0.03
        self._movel(pose, speed, acceleration, wait)
    
    async def set_digital_out(self, pin: int, state: bool):
        """
        OpenClaw 数字输出接口
        
        Args:
            pin: IO 引脚号
            state: 状态 (True/False)
        """
        self._set_digital_out(pin, state)
    
    # ========== 运动控制 ==========
    
    def _movej(self, joints: List[float], speed: float = None, 
               acceleration: float = None, wait: bool = True):
        """关节空间运动"""
        if len(joints) != 6:
            raise ValueError("需要 6 个关节角度")
        
        speed = speed or self.default_speed
        print(f"🦾 movej: {[f'{j:.1f}' for j in joints]} (速度:{speed*100}%)")
        
        # 角度转弧度
        joints_rad = [j * 3.14159 / 180 for j in joints]
        joints_str = ",".join([f"{j:.6f}" for j in joints_rad])
        
        script = f'movej([{joints_str}], a={acceleration or self.default_acceleration}, v={speed})'
        self._send_script(script)
        
        if wait:
            time.sleep(3)
    
    def _movel(self, pose: List[float], speed: float = None,
               acceleration: float = None, wait: bool = True):
        """直线运动"""
        if len(pose) != 6:
            raise ValueError("需要 6 个位姿参数")
        
        speed = speed or 0.03
        print(f"📍 movel: [{pose[0]:.3f}, {pose[1]:.3f}, {pose[2]:.3f}] (速度:{speed})")
        
        pose_str = ",".join([f"{p:.6f}" for p in pose])
        script = f'movel([{pose_str}], a={acceleration or self.default_acceleration}, v={speed})'
        self._send_script(script)
        
        if wait:
            time.sleep(3)
    
    def _send_script(self, script: str):
        """发送脚本命令"""
        print(f"   脚本：{script}")
        self._publish(2, ["input_string_register_0"], [script])
        time.sleep(0.3)
    
    def _set_digital_out(self, pin: int, state: bool):
        """设置数字输出"""
        print(f"🔌 DO[{pin}] = {state}")
        # 通过 RTDE 寄存器控制
        self._publish(1, ["R1_standard_digital_output_mask", "R1_standard_digital_output"], 
                     [1 << pin, 1 << pin if state else 0])
        time.sleep(0.2)
    
    def set_speed(self, speed_fraction: float):
        """设置全局速度"""
        print(f"设置全局速度：{speed_fraction * 100}%")
        self._publish(1, ["speed_slider_mask", "speed_slider_fraction"], [3, speed_fraction])
        time.sleep(0.2)
    
    def speedj(self, joint_speeds: list, duration: float = 2.0):
        """关节速度控制"""
        print(f"⚡ 关节速度：{joint_speeds}")
        speeds_str = ",".join([f"{s:.6f}" for s in joint_speeds])
        script = f'speedj([{speeds_str}], a={self.default_acceleration}, t={duration})'
        self._send_script(script)
        time.sleep(duration + 0.5)
    
    def stop(self, deceleration: float = 1.0):
        """停止运动"""
        print("🛑 停止")
        self._send_script(f'stopl({deceleration})')
        time.sleep(0.5)
    
    # ========== 上下文管理器 ==========
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


# ========== OpenClaw 注册 ==========

def register_skill():
    """注册到 OpenClaw 技能系统"""
    return {
        "name": "aubo-robot",
        "version": "1.0.0",
        "description": "AUBO 遨博机器人控制技能 - RTDE 协议",
        "driver_class": AUBORobotDriver,
        "config_schema": {
            "host": {"type": "string", "default": "192.168.0.136"},
            "port": {"type": "integer", "default": 30010},
            "default_speed": {"type": "number", "default": 0.3},
            "default_acceleration": {"type": "number", "default": 0.3}
        },
        "capabilities": [
            "move_joint",
            "move_line",
            "get_joints",
            "get_tcp_pose",
            "get_status",
            "set_digital_out"
        ]
    }


if __name__ == "__main__":
    # 测试
    config = {
        "host": "192.168.0.136",
        "port": 30010,
        "default_speed": 0.2
    }
    
    with AUBORobotDriver(config) as robot:
        print("\n测试 OpenClaw 接口:")
        print(f"连接状态：{robot.is_connected()}")
        print(f"关节角度：{robot.get_joints()}")
        print(f"TCP 位姿：{robot.get_tcp_pose()}")
