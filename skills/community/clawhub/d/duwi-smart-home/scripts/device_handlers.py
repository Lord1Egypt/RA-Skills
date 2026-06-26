#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备控制处理器模块
使用策略模式实现不同设备类型的控制逻辑
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from duwi_client import DuwiClient


class DeviceHandler(ABC):
    """设备处理器基类"""

    @abstractmethod
    def supports(self, device_type_no: str) -> bool:
        """判断是否支持该设备类型"""
        pass

    @abstractmethod
    def handle(
        self,
        client: DuwiClient,
        house_no: str,
        device: Dict[str, Any],
        action: str,
        value: str,
    ) -> bool:
        """处理设备控制命令"""
        pass

    def _send_command(
        self,
        client: DuwiClient,
        house_no: str,
        device_no: str,
        code: str,
        value: Any,
    ) -> bool:
        """发送设备命令"""
        return client.device_command(house_no, device_no, [{"code": code, "value": value}])

    def _handle_switch(
        self,
        client: DuwiClient,
        house_no: str,
        device_no: str,
        device_name: str,
        value: str,
        code: str = "switch",
    ) -> bool:
        """处理开关命令"""
        if value not in ["on", "off"]:
            return False
        self._send_command(client, house_no, device_no, code, value)
        status = "开启" if value == "on" else "关闭"
        print(f"✅ 已{status} - 设备：{device_name}-{device_no}")
        return True

    def _handle_int_value(
        self,
        client: DuwiClient,
        house_no: str,
        device_no: str,
        device_name: str,
        value: str,
        code: str,
        desc: str,
        min_val: Optional[int] = None,
        max_val: Optional[int] = None,
    ) -> bool:
        """处理整数值命令（如温度、亮度）"""
        try:
            int_val = int(value)
            if min_val is not None and max_val is not None:
                if not min_val <= int_val <= max_val:
                    print(f"⚠️ 设备 {device_name}-{device_no}: {desc}超出范围 ({min_val}-{max_val})")
                    return False
            self._send_command(client, house_no, device_no, code, int_val)
            unit = "℃" if "temp" in code else "%"
            print(f"✅ 已设置{desc}：{int_val}{unit} - 设备：{device_name}-{device_no}")
            return True
        except ValueError:
            print(f"⚠️ 设备 {device_name}-{device_no}: 无效的{desc}值")
            return False

    def _handle_command(
        self,
        client: DuwiClient,
        house_no: str,
        device_no: str,
        device_name: str,
        code: str,
        value: str,
        desc: str,
    ) -> bool:
        """处理枚举命令（如模式、风速）"""
        self._send_command(client, house_no, device_no, code, value)
        print(f"✅ 已设置{desc}：{value} - 设备：{device_name}-{device_no}")
        return True


class SwitchHandler(DeviceHandler):
    """电源断路器处理器"""

    def supports(self, device_type_no: str) -> bool:
        return device_type_no.startswith("1")

    def handle(
        self,
        client: DuwiClient,
        house_no: str,
        device: Dict[str, Any],
        action: str,
        value: str,
    ) -> bool:
        device_no = device.get("deviceNo")
        device_name = device.get("deviceName", "未知")

        if not device_no:
            print(f"⚠️ 设备 {device_name}: 设备编号无效")
            return False

        if action != "switch":
            print(f"⚠️ 设备 {device_name}-{device_no}: 不支持该操作")
            return False

        if value not in ["on", "off"]:
            print(f"⚠️ 设备 {device_name}-{device_no}: 无效的开关操作")
            return False

        self._send_command(client, house_no, device_no, "switch", value)
        status = "开启" if value == "on" else "关闭"
        print(f"✅ 已{status} - 设备：{device_name}-{device_no}")
        return True


class LightHandler(DeviceHandler):
    """灯光处理器"""

    def supports(self, device_type_no: str) -> bool:
        return device_type_no.startswith("3")

    def handle(
        self,
        client: DuwiClient,
        house_no: str,
        device: Dict[str, Any],
        action: str,
        value: str,
    ) -> bool:
        device_no = device.get("deviceNo")
        device_name = device.get("deviceName", "未知")

        if not device_no:
            print(f"⚠️ 设备 {device_name}: 设备编号无效")
            return False

        if action == "switch":
            if value not in ["on", "off"]:
                print(f"⚠️ 设备 {device_name}-{device_no}: 无效的开关操作")
                return False
            self._send_command(client, house_no, device_no, "switch", value)
            status = "开启" if value == "on" else "关闭"
            print(f"✅ 已{status} - 设备：{device_name}-{device_no}")
            return True

        elif action == "light":
            try:
                brightness = int(value)
                if not 0 <= brightness <= 100:
                    print(f"⚠️ 设备 {device_name}-{device_no}: 亮度值超出范围 (0-100%)")
                    return False
                self._send_command(client, house_no, device_no, "light", brightness)
                print(f"✅ 已设置亮度：{brightness}% - 设备：{device_name}-{device_no}")
                return True
            except ValueError:
                print(f"⚠️ 设备 {device_name}-{device_no}: 无效的亮度值")
                return False

        elif action == "color_temp":
            try:
                color_temp = int(value)
                if not 2700 <= color_temp <= 6200:
                    print(f"⚠️ 设备 {device_name}-{device_no}: 色温值超出范围 (2700-6200K)")
                    return False
                self._send_command(client, house_no, device_no, "color_temp", color_temp)
                print(f"✅ 已设置色温：{color_temp}K - 设备：{device_name}-{device_no}")
                return True
            except ValueError:
                print(f"⚠️ 设备 {device_name}-{device_no}: 无效的色温值")
                return False

        elif action == "color":
            color_parts = value.split(":")
            if len(color_parts) != 3:
                print(f"⚠️ 设备 {device_name}-{device_no}: 颜色格式错误，应为 h:s:v")
                return False
            try:
                h, s, v = map(int, color_parts)
                color_value = {"h": h, "s": s, "v": v}
                self._send_command(client, house_no, device_no, "color", color_value)
                print(f"✅ 已设置颜色 - 设备：{device_name}-{device_no}")
                return True
            except ValueError:
                print(f"⚠️ 设备 {device_name}-{device_no}: 无效的颜色值")
                return False

        print(f"⚠️ 设备 {device_name}-{device_no}: 不支持该操作")
        return False


class CurtainHandler(DeviceHandler):
    """窗帘处理器"""

    def supports(self, device_type_no: str) -> bool:
        return device_type_no.startswith("4")

    def handle(
        self,
        client: DuwiClient,
        house_no: str,
        device: Dict[str, Any],
        action: str,
        value: str,
    ) -> bool:
        device_no = device.get("deviceNo")
        device_name = device.get("deviceName", "未知")

        if not device_no:
            print(f"⚠️ 设备 {device_name}: 设备编号无效")
            return False

        if action == "control":
            if value not in ["open", "close", "stop"]:
                print(f"⚠️ 设备 {device_name}-{device_no}: 无效的窗帘操作")
                return False
            self._send_command(client, house_no, device_no, "control", value)
            status_map = {"open": "开启", "close": "关闭", "stop": "停止"}
            print(f"✅ 已{status_map[value]} - 设备：{device_name}-{device_no}")
            return True

        elif action == "control_percent":
            try:
                percent = int(value)
                if not 0 <= percent <= 100:
                    print(f"⚠️ 设备 {device_name}-{device_no}: 开合度超出范围 (0-100%)")
                    return False
                self._send_command(client, house_no, device_no, "control_percent", percent)
                print(f"✅ 已设置开合度：{percent}% - 设备：{device_name}-{device_no}")
                return True
            except ValueError:
                print(f"⚠️ 设备 {device_name}-{device_no}: 无效的开合度值")
                return False

        print(f"⚠️ 设备 {device_name}-{device_no}: 不支持该操作")
        return False


class AirConditionHandler(DeviceHandler):
    """空调处理器"""

    def supports(self, device_type_no: str) -> bool:
        return device_type_no.startswith("5-001")

    def handle(
        self,
        client: DuwiClient,
        house_no: str,
        device: Dict[str, Any],
        action: str,
        value: str,
    ) -> bool:
        device_no = device.get("deviceNo")
        device_name = device.get("deviceName", "未知")

        if not device_no:
            print(f"⚠️ 设备 {device_name}: 设备编号无效")
            return False

        if action == "ac_switch":
            return self._handle_switch(client, house_no, device_no, device_name, value, "ac_switch")
        elif action == "ac_mode":
            return self._handle_command(client, house_no, device_no, device_name, "ac_mode", value, "模式")
        elif action == "ac_set_temp":
            return self._handle_int_value(client, house_no, device_no, device_name, value, "ac_set_temp", "温度", 5, 35)
        elif action == "ac_wind_speed":
            return self._handle_command(client, house_no, device_no, device_name, "ac_wind_speed", value, "风速")
        elif action == "ac_wind_direction":
            return self._handle_command(client, house_no, device_no, device_name, "ac_wind_direction", value, "风向")
        elif action == "ac_lock_mode":
            return self._handle_command(client, house_no, device_no, device_name, "ac_lock_mode", value, "锁定模式")

        print(f"⚠️ 设备 {device_name}-{device_no}: 不支持该操作")
        return False


class FloorHeatHandler(DeviceHandler):
    """地暖处理器"""

    def supports(self, device_type_no: str) -> bool:
        return device_type_no.startswith("5-002")

    def handle(
        self,
        client: DuwiClient,
        house_no: str,
        device: Dict[str, Any],
        action: str,
        value: str,
    ) -> bool:
        device_no = device.get("deviceNo")
        device_name = device.get("deviceName", "未知")

        if not device_no:
            print(f"⚠️ 设备 {device_name}: 设备编号无效")
            return False

        if action == "fh_switch":
            return self._handle_switch(client, house_no, device_no, device_name, value, "fh_switch")
        elif action == "fh_set_temp":
            return self._handle_int_value(client, house_no, device_no, device_name, value, "fh_set_temp", "温度", 10, 30)
        elif action == "fh_lock_mode":
            return self._handle_command(client, house_no, device_no, device_name, "fh_lock_mode", value, "锁定模式")

        print(f"⚠️ 设备 {device_name}-{device_no}: 不支持该操作")
        return False


class FreshAirHandler(DeviceHandler):
    """新风处理器"""

    def supports(self, device_type_no: str) -> bool:
        return device_type_no.startswith("5-003")

    def handle(
        self,
        client: DuwiClient,
        house_no: str,
        device: Dict[str, Any],
        action: str,
        value: str,
    ) -> bool:
        device_no = device.get("deviceNo")
        device_name = device.get("deviceName", "未知")

        if not device_no:
            print(f"⚠️ 设备 {device_name}: 设备编号无效")
            return False

        if action == "fa_switch":
            return self._handle_switch(client, house_no, device_no, device_name, value, "fa_switch")
        elif action == "fa_set_humidity":
            return self._handle_int_value(client, house_no, device_no, device_name, value, "fa_set_humidity", "湿度", 0, 100)
        elif action == "fa_clean_switch":
            return self._handle_switch(client, house_no, device_no, device_name, value, "fa_clean_switch")
        elif action == "fa_work_mode":
            return self._handle_command(client, house_no, device_no, device_name, "fa_work_mode", value, "工作模式")
        elif action == "fa_wind_speed":
            return self._handle_command(client, house_no, device_no, device_name, "fa_wind_speed", value, "风速")
        elif action == "fa_fan_speed":
            return self._handle_command(client, house_no, device_no, device_name, "fa_fan_speed", value, "排风风速")

        print(f"⚠️ 设备 {device_name}-{device_no}: 不支持该操作")
        return False


class HeatPumpHandler(DeviceHandler):
    """热泵处理器"""

    def supports(self, device_type_no: str) -> bool:
        return device_type_no.startswith("5-004")

    def handle(
        self,
        client: DuwiClient,
        house_no: str,
        device: Dict[str, Any],
        action: str,
        value: str,
    ) -> bool:
        device_no = device.get("deviceNo")
        device_name = device.get("deviceName", "未知")

        if not device_no:
            print(f"⚠️ 设备 {device_name}: 设备编号无效")
            return False

        if action == "hp_switch":
            return self._handle_switch(client, house_no, device_no, device_name, value, "hp_switch")
        elif action == "hp_set_temp":
            return self._handle_int_value(client, house_no, device_no, device_name, value, "hp_set_temp", "温度", 5, 55)
        elif action == "hp_mode":
            return self._handle_command(client, house_no, device_no, device_name, "hp_mode", value, "模式")

        print(f"⚠️ 设备 {device_name}-{device_no}: 不支持该操作")
        return False


class TempControlHandler(DeviceHandler):
    """温控（二联供）处理器"""

    def supports(self, device_type_no: str) -> bool:
        return device_type_no.startswith("5-005")

    def handle(
        self,
        client: DuwiClient,
        house_no: str,
        device: Dict[str, Any],
        action: str,
        value: str,
    ) -> bool:
        device_no = device.get("deviceNo")
        device_name = device.get("deviceName", "未知")

        if not device_no:
            print(f"⚠️ 设备 {device_name}: 设备编号无效")
            return False

        if action == "tc_switch":
            return self._handle_switch(client, house_no, device_no, device_name, value, "tc_switch")
        elif action == "tc_set_temp":
            return self._handle_int_value(client, house_no, device_no, device_name, value, "tc_set_temp", "温度", 5, 35)
        elif action == "tc_set_humidity":
            return self._handle_int_value(client, house_no, device_no, device_name, value, "tc_set_humidity", "湿度", 0, 100)
        elif action == "tc_mode":
            return self._handle_command(client, house_no, device_no, device_name, "tc_mode", value, "模式")
        elif action == "tc_wind_speed":
            return self._handle_command(client, house_no, device_no, device_name, "tc_wind_speed", value, "风速")
        elif action == "tc_lock_mode":
            return self._handle_command(client, house_no, device_no, device_name, "tc_lock_mode", value, "锁定模式")

        print(f"⚠️ 设备 {device_name}-{device_no}: 不支持该操作")
        return False


class DeviceHandlerFactory:
    """设备处理器工厂"""

    _handlers: List[DeviceHandler] = [
        SwitchHandler(),
        LightHandler(),
        CurtainHandler(),
        AirConditionHandler(),
        FloorHeatHandler(),
        FreshAirHandler(),
        HeatPumpHandler(),
        TempControlHandler(),
    ]

    @classmethod
    def get_handler(cls, device_type_no: str) -> Optional[DeviceHandler]:
        """获取对应设备类型的处理器"""
        for handler in cls._handlers:
            if handler.supports(device_type_no):
                return handler
        return None

    @classmethod
    def register_handler(cls, handler: DeviceHandler):
        """注册新的设备处理器"""
        cls._handlers.append(handler)
