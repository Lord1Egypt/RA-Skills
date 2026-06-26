#!/usr/bin/env python3
"""
FFmpeg Master - Preset Manager
预设模板管理器，负责加载、验证和管理视频编码预设
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class PresetConfig:
    """预设配置数据类"""

    name: str
    description: str
    version: str
    video: dict
    audio: dict
    recommendations: dict = field(default_factory=dict)
    requirements: dict = field(default_factory=dict)
    platforms: dict = field(default_factory=dict)
    use_cases: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "video": self.video,
            "audio": self.audio,
            "recommendations": self.recommendations,
            "requirements": self.requirements,
            "platforms": self.platforms,
            "use_cases": self.use_cases,
        }


class PresetManager:
    """
    预设模板管理器

    功能：
    1. 列出所有可用预设（内置 + 用户自定义）
    2. 加载并验证预设配置
    3. 创建自定义预设
    4. 验证预设有效性
    """

    # 内置预设目录
    BUILTIN_PRESETS_DIR = Path(__file__).parent.parent.parent / "assets" / "presets"

    # 用户预设目录
    USER_PRESETS_DIR = Path.home() / ".config" / "ffmpeg-master" / "presets"

    # 必需字段
    REQUIRED_FIELDS = ["name", "description", "video", "audio"]

    # 推荐字段
    OPTIONAL_FIELDS = ["version", "recommendations", "requirements", "platforms", "use_cases"]

    def __init__(self):
        """初始化预设管理器"""
        self._ensure_user_presets_dir()

    def _ensure_user_presets_dir(self):
        """确保用户预设目录存在"""
        self.USER_PRESETS_DIR.mkdir(parents=True, exist_ok=True)

    def list_presets(
        self, include_builtin: bool = True, include_custom: bool = True
    ) -> Dict[str, Dict[str, Any]]:
        """
        列出所有可用预设

        Args:
            include_builtin: 是否包含内置预设
            include_custom: 是否包含用户自定义预设

        Returns:
            预设字典，格式：{preset_name: {path, type, metadata}}
        """
        presets = {}

        # 加载内置预设
        if include_builtin and self.BUILTIN_PRESETS_DIR.exists():
            for preset_file in self.BUILTIN_PRESETS_DIR.glob("*.json"):
                try:
                    metadata = self._load_preset_metadata(preset_file)
                    if metadata:
                        presets[preset_file.stem] = {
                            "path": str(preset_file),
                            "type": "builtin",
                            "metadata": metadata,
                        }
                except Exception as e:
                    print(f"警告: 无法加载预设 {preset_file.name}: {e}")

        # 加载用户预设
        if include_custom and self.USER_PRESETS_DIR.exists():
            for preset_file in self.USER_PRESETS_DIR.glob("*.json"):
                try:
                    metadata = self._load_preset_metadata(preset_file)
                    if metadata:
                        presets[preset_file.stem] = {
                            "path": str(preset_file),
                            "type": "custom",
                            "metadata": metadata,
                        }
                except Exception as e:
                    print(f"警告: 无法加载预设 {preset_file.name}: {e}")

        return presets

    def _load_preset_metadata(self, preset_file: Path) -> Optional[Dict[str, Any]]:
        """
        加载预设元数据（仅基本信息）

        Args:
            preset_file: 预设文件路径

        Returns:
            预设元数据字典
        """
        try:
            with open(preset_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            return {
                "name": data.get("name", preset_file.stem),
                "description": data.get("description", ""),
                "version": data.get("version", "1.0"),
            }
        except Exception:
            return None

    def load_preset(self, preset_name: str) -> Optional[PresetConfig]:
        """
        加载指定预设

        Args:
            preset_name: 预设名称（不含.json后缀）

        Returns:
            PresetConfig 对象，如果加载失败返回 None
        """
        # 首先尝试用户预设
        user_preset = self.USER_PRESETS_DIR / f"{preset_name}.json"
        if user_preset.exists():
            return self._load_preset_from_file(user_preset)

        # 然后尝试内置预设
        builtin_preset = self.BUILTIN_PRESETS_DIR / f"{preset_name}.json"
        if builtin_preset.exists():
            return self._load_preset_from_file(builtin_preset)

        print(f"错误: 找不到预设 '{preset_name}'")
        return None

    def _load_preset_from_file(self, preset_file: Path) -> Optional[PresetConfig]:
        """
        从文件加载预设

        Args:
            preset_file: 预设文件路径

        Returns:
            PresetConfig 对象
        """
        try:
            with open(preset_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 验证预设
            if not self.validate_preset(data):
                return None

            # 创建 PresetConfig 对象
            return PresetConfig(
                name=data["name"],
                description=data["description"],
                version=data.get("version", "1.0"),
                video=data["video"],
                audio=data["audio"],
                recommendations=data.get("recommendations", {}),
                requirements=data.get("requirements", {}),
                platforms=data.get("platforms", {}),
                use_cases=data.get("use_cases", []),
            )
        except Exception as e:
            print(f"错误: 无法加载预设文件 {preset_file.name}: {e}")
            return None

    def create_custom_preset(self, preset_name: str, config: PresetConfig) -> bool:
        """
        创建自定义预设

        Args:
            preset_name: 预设名称（不含.json后缀）
            config: PresetConfig 对象

        Returns:
            是否成功创建
        """
        try:
            # 验证配置
            config_dict = config.to_dict()
            if not self.validate_preset(config_dict):
                print("错误: 预设配置无效")
                return False

            # 保存到用户预设目录
            preset_file = self.USER_PRESETS_DIR / f"{preset_name}.json"
            with open(preset_file, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, ensure_ascii=False, indent=2)

            print(f"成功: 自定义预设已保存: {preset_file.name}")
            return True
        except Exception as e:
            print(f"错误: 无法创建自定义预设: {e}")
            return False

    def validate_preset(self, preset_data: dict) -> bool:
        """
        验证预设配置

        Args:
            preset_data: 预设配置字典

        Returns:
            是否有效
        """
        # 检查必需字段
        for field in self.REQUIRED_FIELDS:
            if field not in preset_data:
                print(f"错误: 缺少必需字段 '{field}'")
                return False

        # 验证视频配置
        video = preset_data.get("video", {})
        if not self._validate_video_config(video):
            return False

        # 验证音频配置
        audio = preset_data.get("audio", {})
        if not self._validate_audio_config(audio):
            return False

        return True

    def _validate_video_config(self, video: dict) -> bool:
        """验证视频配置"""
        required_video_fields = ["codec", "preset", "crf"]
        for field in required_video_fields:
            if field not in video:
                print(f"错误: 视频配置缺少必需字段 '{field}'")
                return False

        # 验证 CRF 值范围（0-51）
        crf = video.get("crf")
        if not isinstance(crf, int) or crf < 0 or crf > 51:
            print(f"错误: 无效的 CRF 值 {crf}，必须在 0-51 之间")
            return False

        return True

    def _validate_audio_config(self, audio: dict) -> bool:
        """验证音频配置"""
        required_audio_fields = ["codec"]
        for field in required_audio_fields:
            if field not in audio:
                print(f"错误: 音频配置缺少必需字段 '{field}'")
                return False

        return True

    def get_preset_names(self) -> List[str]:
        """
        获取所有可用预设名称

        Returns:
            预设名称列表
        """
        presets = self.list_presets()
        return sorted(presets.keys())

    def search_presets(self, keyword: str) -> List[str]:
        """
        搜索预设（按名称或描述）

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的预设名称列表
        """
        presets = self.list_presets()
        keyword_lower = keyword.lower()

        matched = []
        for name, info in presets.items():
            metadata = info["metadata"]
            # 搜索名称和描述
            if keyword_lower in name.lower() or keyword_lower in metadata["description"].lower():
                matched.append(name)

        return sorted(matched)

    def delete_custom_preset(self, preset_name: str) -> bool:
        """
        删除用户自定义预设

        Args:
            preset_name: 预设名称

        Returns:
            是否成功删除
        """
        try:
            preset_file = self.USER_PRESETS_DIR / f"{preset_name}.json"
            if preset_file.exists():
                preset_file.unlink()
                print(f"成功: 已删除预设 '{preset_name}'")
                return True
            else:
                print(f"错误: 找不到自定义预设 '{preset_name}'")
                return False
        except Exception as e:
            print(f"错误: 无法删除预设: {e}")
            return False

    def get_preset_info(self, preset_name: str) -> Optional[Dict[str, Any]]:
        """
        获取预设详细信息

        Args:
            preset_name: 预设名称

        Returns:
            预设信息字典
        """
        config = self.load_preset(preset_name)
        if config is None:
            return None

        return {
            "name": config.name,
            "description": config.description,
            "version": config.version,
            "video": config.video,
            "audio": config.audio,
            "recommendations": config.recommendations,
            "requirements": config.requirements,
            "platforms": config.platforms,
            "use_cases": config.use_cases,
        }


# 导出
__all__ = ["PresetManager", "PresetConfig"]
