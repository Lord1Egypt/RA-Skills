"""
音色库管理 — 参考音频注册 + 音色档案管理
支持本地音色库 + Fish Speech API 注册
"""

import os
import json
import shutil
import requests
from typing import List, Optional, Dict
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class VoiceProfile:
    """音色档案"""
    id: str  # 音色 ID（英文，用于 API）
    name: str  # 显示名称
    description: str  # 描述
    gender: str  # male/female/neutral
    age_range: str  # 年龄段（如 "20-30"）
    language: str  # 主要语言（zh/en/ja）
    emotion_tags: List[str]  # 擅长的情绪
    ref_audio_path: str  # 本地参考音频路径
    ref_text: Optional[str] = None  # 参考音频对应文本
    registered: bool = False  # 是否已注册到 Fish Speech
    metadata: Dict = None  # 其他元数据
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.emotion_tags is None:
            self.emotion_tags = []


class VoiceLibrary:
    """
    音色库管理器
    
    功能：
    1. 本地音色档案存储（JSON）
    2. 参考音频文件管理
    3. Fish Speech API 注册/注销
    4. 音色搜索和筛选
    """
    
    def __init__(
        self,
        library_dir: str = "voice_profiles",
        api_base: str = "http://127.0.0.1:18791"
    ):
        self.library_dir = Path(library_dir)
        self.library_dir.mkdir(parents=True, exist_ok=True)
        self.api_base = api_base
        
        # 音色档案文件
        self.profiles_file = self.library_dir / "voices.json"
        self.profiles = self._load_profiles()
        
        # 参考音频目录
        self.audio_dir = self.library_dir / "audio"
        self.audio_dir.mkdir(exist_ok=True)
    
    def _load_profiles(self) -> Dict[str, VoiceProfile]:
        """加载音色档案"""
        if not self.profiles_file.exists():
            return {}
        
        try:
            with open(self.profiles_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    k: VoiceProfile(**v)
                    for k, v in data.items()
                }
        except Exception as e:
            print(f"警告: 加载音色档案失败: {e}")
            return {}
    
    def _save_profiles(self):
        """保存音色档案"""
        data = {
            k: asdict(v)
            for k, v in self.profiles.items()
        }
        with open(self.profiles_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_voice(
        self,
        voice_id: str,
        name: str,
        ref_audio_path: str,
        description: str = "",
        gender: str = "neutral",
        age_range: str = "",
        language: str = "zh",
        emotion_tags: List[str] = None,
        ref_text: str = None,
        metadata: Dict = None
    ) -> VoiceProfile:
        """
        添加新音色到本地库
        
        Args:
            voice_id: 音色 ID（英文，如 "momo_happy"）
            name: 显示名称（如 "MOMO-开心"）
            ref_audio_path: 参考音频文件路径
            description: 描述
            gender: 性别
            age_range: 年龄段
            language: 语言
            emotion_tags: 情绪标签
            ref_text: 参考音频对应文本
            metadata: 其他元数据
        
        Returns:
            VoiceProfile: 创建的音色档案
        """
        # 验证音频文件
        if not os.path.exists(ref_audio_path):
            raise FileNotFoundError(f"参考音频不存在: {ref_audio_path}")
        
        # 复制音频到库目录
        audio_filename = f"{voice_id}.mp3"
        dest_audio_path = self.audio_dir / audio_filename
        shutil.copy2(ref_audio_path, dest_audio_path)
        
        # 创建档案
        profile = VoiceProfile(
            id=voice_id,
            name=name,
            description=description,
            gender=gender,
            age_range=age_range,
            language=language,
            emotion_tags=emotion_tags or [],
            ref_audio_path=str(dest_audio_path),
            ref_text=ref_text,
            metadata=metadata or {}
        )
        
        # 保存
        self.profiles[voice_id] = profile
        self._save_profiles()
        
        print(f"✅ 音色已添加到本地库: {name} ({voice_id})")
        return profile
    
    def register_to_api(self, voice_id: str) -> bool:
        """
        注册音色到 Fish Speech API
        
        Args:
            voice_id: 音色 ID
        
        Returns:
            bool: 是否成功
        """
        if voice_id not in self.profiles:
            print(f"错误: 音色不存在: {voice_id}", file=__import__('sys').stderr)
            return False
        
        profile = self.profiles[voice_id]
        
        # 检查音频文件
        if not os.path.exists(profile.ref_audio_path):
            print(f"错误: 参考音频不存在: {profile.ref_audio_path}", file=__import__('sys').stderr)
            return False
        
        # 调用 API
        try:
            with open(profile.ref_audio_path, "rb") as f:
                files = {"audio": (os.path.basename(profile.ref_audio_path), f)}
                # API 要求 ref_text 不能为空，如果没有提供则使用占位符
                ref_text = profile.ref_text if profile.ref_text else "参考音频"
                data = {
                    "id": voice_id,
                    "text": ref_text
                }
                
                r = requests.post(
                    f"{self.api_base}/v1/references/add",
                    files=files,
                    data=data,
                    timeout=30
                )
            
            if r.status_code == 200:
                profile.registered = True
                self._save_profiles()
                print(f"✅ 音色已注册到 API: {voice_id}")
                return True
            else:
                print(f"错误: API 注册失败 ({r.status_code}): {r.text}", file=__import__('sys').stderr)
                return False
        
        except Exception as e:
            print(f"错误: API 请求失败: {e}", file=__import__('sys').stderr)
            return False
    
    def unregister_from_api(self, voice_id: str) -> bool:
        """从 Fish Speech API 注销音色"""
        try:
            r = requests.delete(
                f"{self.api_base}/v1/references/delete",
                json={"reference_id": voice_id},
                timeout=10
            )
            
            if r.status_code == 200:
                if voice_id in self.profiles:
                    self.profiles[voice_id].registered = False
                    self._save_profiles()
                print(f"✅ 音色已从 API 注销: {voice_id}")
                return True
            else:
                print(f"错误: API 注销失败 ({r.status_code}): {r.text}", file=__import__('sys').stderr)
                return False
        
        except Exception as e:
            print(f"错误: API 请求失败: {e}", file=__import__('sys').stderr)
            return False
    
    def remove_voice(self, voice_id: str, delete_audio: bool = False):
        """
        从本地库移除音色
        
        Args:
            voice_id: 音色 ID
            delete_audio: 是否删除音频文件
        """
        if voice_id not in self.profiles:
            print(f"警告: 音色不存在: {voice_id}")
            return
        
        profile = self.profiles[voice_id]
        
        # 如果已注册到 API，先注销
        if profile.registered:
            self.unregister_from_api(voice_id)
        
        # 删除音频文件
        if delete_audio and os.path.exists(profile.ref_audio_path):
            try:
                os.remove(profile.ref_audio_path)
                print(f"✅ 音频文件已删除: {profile.ref_audio_path}")
            except Exception as e:
                print(f"警告: 无法删除音频文件: {e}")
        
        # 从档案中移除
        del self.profiles[voice_id]
        self._save_profiles()
        print(f"✅ 音色已从本地库移除: {voice_id}")
    
    def get_voice(self, voice_id: str) -> Optional[VoiceProfile]:
        """获取音色档案"""
        return self.profiles.get(voice_id)
    
    def list_voices(
        self,
        gender: Optional[str] = None,
        language: Optional[str] = None,
        emotion: Optional[str] = None,
        registered_only: bool = False
    ) -> List[VoiceProfile]:
        """
        列出音色（支持筛选）
        
        Args:
            gender: 按性别筛选
            language: 按语言筛选
            emotion: 按情绪标签筛选
            registered_only: 仅显示已注册到 API 的音色
        
        Returns:
            List[VoiceProfile]: 匹配的音色列表
        """
        results = list(self.profiles.values())
        
        if gender:
            results = [v for v in results if v.gender == gender]
        
        if language:
            results = [v for v in results if v.language == language]
        
        if emotion:
            results = [v for v in results if emotion in v.emotion_tags]
        
        if registered_only:
            results = [v for v in results if v.registered]
        
        return results
    
    def search(self, query: str) -> List[VoiceProfile]:
        """搜索音色（按名称/描述）"""
        query = query.lower()
        results = []
        for profile in self.profiles.values():
            if (query in profile.name.lower() or
                query in profile.description.lower() or
                query in profile.id.lower()):
                results.append(profile)
        return results
    
    def sync_with_api(self):
        """
        同步本地库与 API
        
        检查哪些本地音色未注册到 API，自动注册
        """
        # 获取 API 上已注册的音色
        try:
            r = requests.get(f"{self.api_base}/v1/references/list", timeout=10)
            if r.status_code == 200:
                # API 返回 msgpack 格式
                try:
                    import ormsgpack
                    data = ormsgpack.unpackb(r.content)
                except:
                    data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
                
                api_voices = set(data.get("reference_ids", []))
            else:
                api_voices = set()
        except Exception as e:
            print(f"警告: 无法获取 API 音色列表: {e}")
            api_voices = set()
        
        # 检查本地音色
        unregistered = []
        for voice_id, profile in self.profiles.items():
            if voice_id in api_voices:
                if not profile.registered:
                    profile.registered = True
                    self._save_profiles()
            elif profile.registered:
                # 本地标记为已注册，但 API 上没有
                profile.registered = False
                self._save_profiles()
            else:
                # 本地有但未注册
                unregistered.append(profile)
        
        if unregistered:
            print(f"发现 {len(unregistered)} 个未注册的音色:")
            for profile in unregistered:
                print(f"  - {profile.name} ({profile.id})")
        
        return unregistered
    
    def export_to_dict(self) -> Dict:
        """导出所有音色档案为字典"""
        return {k: asdict(v) for k, v in self.profiles.items()}
    
    def import_from_dict(self, data: Dict):
        """从字典导入音色档案"""
        for voice_id, profile_data in data.items():
            self.profiles[voice_id] = VoiceProfile(**profile_data)
        self._save_profiles()
        print(f"✅ 已导入 {len(data)} 个音色档案")


# 便捷函数
def quick_add_voice(
    voice_id: str,
    name: str,
    ref_audio_path: str,
    library_dir: str = "voice_profiles",
    **kwargs
) -> VoiceProfile:
    """快速添加音色"""
    library = VoiceLibrary(library_dir=library_dir)
    return library.add_voice(voice_id, name, ref_audio_path, **kwargs)


if __name__ == "__main__":
    # 测试
    print("测试音色库管理...")
    
    library = VoiceLibrary(library_dir="test_library")
    
    # 列出音色
    voices = library.list_voices()
    print(f"当前有 {len(voices)} 个音色")
    
    # 搜索
    results = library.search("momo")
    print(f"搜索 'momo' 找到 {len(results)} 个结果")
