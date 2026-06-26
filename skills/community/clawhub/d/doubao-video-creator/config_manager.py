#!/usr/bin/env python3
"""
豆包视频创作助手 - 配置管理器
负责 API 配置、模型选择、项目配置的保存和加载
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, Tuple

# 配置路径
GLOBAL_CONFIG_PATH = "/root/.openclaw/workspace/doubao-config.json"
PROJECTS_DIR = "/root/.openclaw/workspace/doubao-video-projects"

# 可用模型列表
AVAILABLE_MODELS = {
    "text_to_video": [
        {"id": "doubao-seedance-2-0-pro", "name": "豆包 Seedance 2.0 Pro", "recommended": True},
        {"id": "doubao-seedance-1-5-pro", "name": "豆包 Seedance 1.5 Pro", "recommended": False},
        {"id": "doubao-seedance-1-0-pro", "name": "豆包 Seedance 1.0 Pro", "recommended": False},
    ],
    "image_to_video": [
        {"id": "doubao-seedance-2-0-pro", "name": "豆包 Seedance 2.0 Pro", "recommended": True},
        {"id": "doubao-seedance-1-5-pro", "name": "豆包 Seedance 1.5 Pro", "recommended": False},
        {"id": "doubao-seedance-1-0-pro", "name": "豆包 Seedance 1.0 Pro", "recommended": False},
    ]
}


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.global_config = self._load_global_config()
    
    def _load_global_config(self) -> Dict:
        """加载全局配置"""
        if os.path.exists(GLOBAL_CONFIG_PATH):
            try:
                with open(GLOBAL_CONFIG_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 加载全局配置失败：{e}")
        
        # 返回默认配置
        return {
            "default_api_key": "",
            "default_text_to_video_model": "doubao-seedance-2-0-pro",
            "default_image_to_video_model": "doubao-seedance-1-5-pro",
            "last_updated": None,
            "is_configured": False
        }
    
    def save_global_config(self, api_key: str, text_model: str, image_model: str):
        """保存全局配置"""
        config = {
            "default_api_key": api_key,
            "default_text_to_video_model": text_model,
            "default_image_to_video_model": image_model,
            "last_updated": datetime.now().isoformat(),
            "is_configured": True
        }
        
        os.makedirs(os.path.dirname(GLOBAL_CONFIG_PATH), exist_ok=True)
        with open(GLOBAL_CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        self.global_config = config
        print(f"✅ 全局配置已保存：{GLOBAL_CONFIG_PATH}")
    
    def is_configured(self) -> bool:
        """检查是否已配置"""
        return self.global_config.get("is_configured", False) and \
               bool(self.global_config.get("default_api_key", ""))
    
    def get_api_key(self) -> str:
        """获取 API Key"""
        return self.global_config.get("default_api_key", "")
    
    def get_text_to_video_model(self) -> str:
        """获取文生视频模型"""
        return self.global_config.get("default_text_to_video_model", "doubao-seedance-2-0-pro")
    
    def get_image_to_video_model(self) -> str:
        """获取图生视频模型"""
        return self.global_config.get("default_image_to_video_model", "doubao-seedance-1-5-pro")
    
    def get_available_models(self, model_type: str) -> list:
        """获取可用模型列表"""
        return AVAILABLE_MODELS.get(model_type, [])
    
    def get_model_choices_prompt(self) -> str:
        """生成模型选择提示"""
        prompt = "请选择模型版本：\n\n"
        
        prompt += "📹 **文生视频模型**：\n"
        for model in AVAILABLE_MODELS["text_to_video"]:
            rec = "（推荐）" if model["recommended"] else ""
            prompt += f"  {model['id']}{rec}\n"
        
        prompt += "\n🖼️ **图生视频模型**：\n"
        for model in AVAILABLE_MODELS["image_to_video"]:
            rec = "（推荐）" if model["recommended"] else ""
            prompt += f"  {model['id']}{rec}\n"
        
        return prompt


class ProjectConfig:
    """项目配置管理"""
    
    def __init__(self, project_id: str, theme: str = ""):
        self.project_id = project_id
        self.project_dir = f"{PROJECTS_DIR}/{project_id}"
        self.config_path = f"{self.project_dir}/project.json"
        
        # 项目数据
        self.data = {
            "project_id": project_id,
            "theme": theme,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "collecting",  # collecting, planning, generating_elements, generating, confirming, completed
            
            # API 配置（可覆盖全局配置）
            "api_config": {
                "api_key": "",
                "text_to_video_model": "",
                "image_to_video_model": "",
                "configured_at": None
            },
            
            # 参考资料
            "references": {
                "documents": [],
                "urls": [],
                "images": [],
                "notes": ""
            },
            
            # 脚本
            "script": None,
            
            # 关键元素
            "key_elements": {
                "characters": [],
                "scenes": [],
                "objects": []
            },
            
            # 场景生成记录
            "scenes": [],
            
            # 最终视频
            "final_video": None,
            
            # 生成日志
            "generation_log": []
        }
        
        # 创建项目目录
        self._ensure_directories()
    
    def _ensure_directories(self):
        """创建项目目录结构"""
        os.makedirs(self.project_dir, exist_ok=True)
        os.makedirs(f"{self.project_dir}/references", exist_ok=True)
        os.makedirs(f"{self.project_dir}/characters", exist_ok=True)
        os.makedirs(f"{self.project_dir}/scenes", exist_ok=True)
        os.makedirs(f"{self.project_dir}/objects", exist_ok=True)
        os.makedirs(f"{self.project_dir}/videos", exist_ok=True)
    
    def load(self) -> bool:
        """加载项目配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                return True
            except Exception as e:
                print(f"⚠️ 加载项目配置失败：{e}")
                return False
        return False
    
    def save(self):
        """保存项目配置"""
        self.data["updated_at"] = datetime.now().isoformat()
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def set_api_config(self, api_key: str, text_model: str, image_model: str):
        """设置 API 配置"""
        self.data["api_config"] = {
            "api_key": api_key,
            "text_to_video_model": text_model,
            "image_to_video_model": image_model,
            "configured_at": datetime.now().isoformat()
        }
        self.save()
    
    def get_api_config(self) -> Tuple[str, str, str]:
        """获取 API 配置（优先使用项目配置，否则使用全局配置）"""
        api_config = self.data.get("api_config", {})
        return (
            api_config.get("api_key", ""),
            api_config.get("text_to_video_model", "doubao-seedance-2-0-pro"),
            api_config.get("image_to_video_model", "doubao-seedance-1-5-pro")
        )
    
    def add_scene(self, scene_data: Dict):
        """添加场景"""
        scene_data["created_at"] = datetime.now().isoformat()
        scene_data["status"] = "pending"  # pending, generating, pending_confirmation, confirmed, rejected
        self.data["scenes"].append(scene_data)
        self.save()
    
    def update_scene(self, scene_id: int, updates: Dict):
        """更新场景"""
        for scene in self.data["scenes"]:
            if scene["id"] == scene_id:
                scene.update(updates)
                scene["updated_at"] = datetime.now().isoformat()
                break
        self.save()
    
    def get_scene(self, scene_id: int) -> Optional[Dict]:
        """获取场景"""
        for scene in self.data["scenes"]:
            if scene["id"] == scene_id:
                return scene
        return None
    
    def get_scene_generation_mode(self, scene_id: int) -> str:
        """获取场景生成方式"""
        scene = self.get_scene(scene_id)
        if scene:
            return scene.get("generation_mode", "text_to_video")
        return "text_to_video"
    
    def set_scene_generation_mode(self, scene_id: int, mode: str, prototype_images: list = None):
        """设置场景生成方式"""
        updates = {
            "generation_mode": mode,
            "prototype_images": prototype_images or []
        }
        self.update_scene(scene_id, updates)
    
    def add_key_element(self, element_type: str, element_data: Dict):
        """添加关键元素"""
        element_data["created_at"] = datetime.now().isoformat()
        element_data["status"] = "pending"  # pending, confirmed, rejected
        self.data["key_elements"][element_type].append(element_data)
        self.save()
    
    def confirm_element(self, element_type: str, element_id: int):
        """确认关键元素"""
        for element in self.data["key_elements"][element_type]:
            if element["id"] == element_id:
                element["status"] = "confirmed"
                element["confirmed_at"] = datetime.now().isoformat()
                break
        self.save()
    
    def reject_element(self, element_type: str, element_id: int, feedback: str):
        """拒绝关键元素"""
        for element in self.data["key_elements"][element_type]:
            if element["id"] == element_id:
                element["status"] = "rejected"
                element["feedback"] = feedback
                element["rejected_at"] = datetime.now().isoformat()
                break
        self.save()
    
    def add_generation_log(self, action: str, details: Dict):
        """添加生成日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }
        self.data["generation_log"].append(log_entry)
        self.save()
    
    def set_status(self, status: str):
        """设置项目状态"""
        self.data["status"] = status
        self.save()
    
    def get_status(self) -> str:
        """获取项目状态"""
        return self.data.get("status", "collecting")
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return self.data.copy()


def get_or_create_project(project_id: str = None, theme: str = "") -> ProjectConfig:
    """获取或创建项目"""
    if project_id is None:
        project_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    project = ProjectConfig(project_id, theme)
    
    # 如果项目已存在，加载配置
    if os.path.exists(project.config_path):
        project.load()
    
    return project


def list_projects() -> list:
    """列出所有项目"""
    projects = []
    if os.path.exists(PROJECTS_DIR):
        for item in os.listdir(PROJECTS_DIR):
            project_path = f"{PROJECTS_DIR}/{item}"
            config_path = f"{project_path}/project.json"
            if os.path.isdir(project_path) and os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        projects.append({
                            "project_id": item,
                            "theme": config.get("theme", ""),
                            "status": config.get("status", ""),
                            "created_at": config.get("created_at", "")
                        })
                except:
                    pass
    return projects


if __name__ == "__main__":
    # 测试
    config_manager = ConfigManager()
    print(f"已配置：{config_manager.is_configured()}")
    print(f"API Key: {config_manager.get_api_key()[:10]}..." if config_manager.get_api_key() else "未配置")
    print(f"文生视频模型：{config_manager.get_text_to_video_model()}")
    print(f"图生视频模型：{config_manager.get_image_to_video_model()}")
    
    # 创建测试项目
    project = get_or_create_project(theme="测试项目")
    print(f"\n项目创建：{project.project_id}")
    print(f"项目目录：{project.project_dir}")
