#!/usr/bin/env python3
"""
豆包视频创作助手 - 完整对话流程
支持用户上传资料、生成脚本、分场景制作、最终合成
"""

import json
import os
from datetime import datetime
from doubao_video_creator import DoubaoVideoCreator

# 项目配置
PROJECT_DIR = "/root/.openclaw/workspace/doubao-video-projects"
os.makedirs(PROJECT_DIR, exist_ok=True)


class VideoProject:
    """视频项目管理"""
    
    def __init__(self, theme, user_id="default"):
        self.project_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.theme = theme
        self.user_id = user_id
        self.created_at = datetime.now().isoformat()
        
        # 项目数据
        self.references = {
            "documents": [],
            "urls": [],
            "images": [],
            "notes": ""
        }
        self.script = None
        self.key_elements = {
            "characters": [],  # 关键人物
            "scenes": [],      # 关键场景
            "objects": []      # 关键物品
        }
        self.scenes = []
        self.final_video = None
        self.status = "collecting"  # collecting, planning, generating_elements, generating, confirming, completed
        
        # 视频生成器
        self.creator = DoubaoVideoCreator()
        
        # 项目目录
        self.project_dir = f"{PROJECT_DIR}/{self.project_id}"
        os.makedirs(self.project_dir, exist_ok=True)
        os.makedirs(f"{self.project_dir}/characters", exist_ok=True)
        os.makedirs(f"{self.project_dir}/scenes", exist_ok=True)
        os.makedirs(f"{self.project_dir}/objects", exist_ok=True)
        os.makedirs(f"{self.project_dir}/videos", exist_ok=True)
    
    def add_reference(self, ref_type, content):
        """添加参考资料"""
        if ref_type == "document":
            self.references["documents"].append(content)
        elif ref_type == "url":
            self.references["urls"].append(content)
        elif ref_type == "image":
            self.references["images"].append(content)
        elif ref_type == "note":
            self.references["notes"] = content
    
    def generate_script(self, total_duration=12, scene_count=3):
        """生成视频脚本（需要 AI 辅助）"""
        # 这里应该调用 AI 分析参考资料并生成脚本
        # 简化示例：返回模板脚本
        
        self.script = {
            "theme": self.theme,
            "total_duration": total_duration,
            "scene_count": scene_count,
            "scenes": [
                {
                    "id": 1,
                    "time": f"0-{total_duration//scene_count}秒",
                    "title": "开场展示",
                    "description": "产品特写，镜头从下往上扫过",
                    "copy": "创新科技，改变生活",
                    "style": "现代科技感",
                    "prompt": "",
                    "video_path": None,
                    "status": "pending"  # pending, generating, confirmed, rejected
                },
                {
                    "id": 2,
                    "time": f"{total_duration//scene_count}-{2*total_duration//scene_count}秒",
                    "title": "功能演示",
                    "description": "产品使用场景，用户操作演示",
                    "copy": "简单便捷，一触即发",
                    "style": "清晰直观",
                    "prompt": "",
                    "video_path": None,
                    "status": "pending"
                },
                {
                    "id": 3,
                    "time": f"{2*total_duration//scene_count}-{total_duration}秒",
                    "title": "品牌结尾",
                    "description": "品牌 Logo + Slogan",
                    "copy": "XXX，值得信赖",
                    "style": "专业大气",
                    "prompt": "",
                    "video_path": None,
                    "status": "pending"
                }
            ]
        }
        
        self.status = "planning"
        self.save()
        return self.script
    
    def update_scene_prompt(self, scene_id, prompt):
        """更新场景提示词"""
        for scene in self.script["scenes"]:
            if scene["id"] == scene_id:
                scene["prompt"] = prompt
                break
        self.save()
    
    def generate_scene_prompt(self, scene_id):
        """
        生成场景视频提示词（基于脚本和参考图）
        
        Args:
            scene_id: 场景 ID
            
        Returns:
            prompt: 生成的提示词
        """
        for scene in self.script["scenes"]:
            if scene["id"] == scene_id:
                # 基于脚本信息和参考图生成详细提示词
                base_prompt = f"{scene['style']}风格，{scene['description']}"
                
                # 如果有确认的参考图，加入提示词
                if self.key_elements.get("scenes"):
                    confirmed_scenes = [s for s in self.key_elements["scenes"] if s["status"] == "confirmed"]
                    if confirmed_scenes:
                        base_prompt += f"，参考已确认的场景风格"
                
                if self.key_elements.get("characters"):
                    confirmed_chars = [c for c in self.key_elements["characters"] if c["status"] == "confirmed"]
                    if confirmed_chars:
                        base_prompt += f"，人物形象参考已确认的主角"
                
                # 添加通用质量词
                base_prompt += "，高清写实，电影级画质，4K 细节，专业摄影"
                
                scene["prompt"] = base_prompt
                self.save()
                return base_prompt
        
        return None
    
    def confirm_scene_prompt(self, scene_id, prompt):
        """确认场景提示词"""
        for scene in self.script["scenes"]:
            if scene["id"] == scene_id:
                scene["prompt"] = prompt
                scene["prompt_confirmed"] = True
                break
        self.save()
    
    def generate_scene_video(self, scene_id):
        """生成场景视频"""
        for scene in self.script["scenes"]:
            if scene["id"] == scene_id:
                if not scene.get("prompt_confirmed"):
                    return False, "提示词未确认"
                
                scene["status"] = "generating"
                self.save()
                
                # 调用视频生成
                success, video_path = self.creator.generate_scene(
                    scene["prompt"],
                    duration=4,
                    scene_id=scene_id
                )
                
                if success:
                    scene["video_path"] = video_path
                    scene["status"] = "pending_confirmation"  # 待用户确认
                else:
                    scene["status"] = "rejected"
                
                self.save()
                return success, video_path
        
        return False, "场景未找到"
    
    def confirm_scene(self, scene_id):
        """确认场景视频"""
        for scene in self.script["scenes"]:
            if scene["id"] == scene_id:
                scene["status"] = "confirmed"
                break
        self.save()
    
    def reject_scene(self, scene_id, feedback):
        """拒绝场景视频（需要重新生成）"""
        for scene in self.script["scenes"]:
            if scene["id"] == scene_id:
                scene["status"] = "rejected"
                scene["feedback"] = feedback
                break
        self.save()
    
    def add_key_element(self, element_type, description, image_path, status="pending"):
        """
        添加关键元素（人物/场景/物品）
        
        Args:
            element_type: "character", "scene", 或 "object"
            description: 元素描述
            image_path: 生成的参考图路径
            status: "pending", "confirmed", "rejected"
        """
        element = {
            "id": len(self.key_elements[element_type]) + 1,
            "description": description,
            "image_path": image_path,
            "status": status,
            "feedback": ""
        }
        
        self.key_elements[element_type].append(element)
        self.save()
        return element
    
    def confirm_element(self, element_type, element_id):
        """确认关键元素"""
        for element in self.key_elements[element_type]:
            if element["id"] == element_id:
                element["status"] = "confirmed"
                break
        self.save()
    
    def reject_element(self, element_type, element_id, feedback):
        """拒绝关键元素（需要重新生成）"""
        for element in self.key_elements[element_type]:
            if element["id"] == element_id:
                element["status"] = "rejected"
                element["feedback"] = feedback
                break
        self.save()
    
    def get_all_elements_confirmed(self):
        """检查所有关键元素是否已确认"""
        for element_type in ["characters", "scenes", "objects"]:
            for element in self.key_elements[element_type]:
                if element["status"] != "confirmed":
                    return False
        return True
    
    def generate_element_image(self, prompt, element_type, description):
        """
        生成关键元素参考图
        
        Args:
            prompt: 图片生成提示词
            element_type: "character", "scene", 或 "object"
            description: 元素描述
            
        Returns:
            (success, image_path): 是否成功和图片路径
        """
        # 调用通义万相 API 生成图片
        # 这里简化示例，实际应调用 wanxiang_generate.py
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if element_type == "character":
            image_path = f"{self.project_dir}/characters/{element_type}_{timestamp}.png"
        elif element_type == "scene":
            image_path = f"{self.project_dir}/scenes/{element_type}_{timestamp}.png"
        else:
            image_path = f"{self.project_dir}/objects/{element_type}_{timestamp}.png"
        
        # TODO: 调用通义万相 API
        # success = wanxiang_generate(prompt, image_path)
        
        # 简化示例：创建空文件
        with open(image_path, "w") as f:
            f.write(f"# {prompt}\n")
        
        success = True  # 示例中假设成功
        
        if success:
            self.add_key_element(element_type, description, image_path)
            return True, image_path
        else:
            return False, None
    
    def save(self):
        """保存项目"""
        data = {
            "project_id": self.project_id,
            "theme": self.theme,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "references": self.references,
            "script": self.script,
            "key_elements": self.key_elements,
            "scenes": self.scenes,
            "final_video": self.final_video,
            "status": self.status
        }
        
        with open(f"{self.project_dir}/project.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self, project_id):
        """加载项目"""
        project_file = f"{PROJECT_DIR}/{project_id}/project.json"
        if os.path.exists(project_file):
            with open(project_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.__dict__.update(data)
                return True
        return False


def format_script_display(script):
    """格式化脚本显示"""
    output = []
    output.append(f"【视频脚本】{script['theme']}")
    output.append(f"总时长：{script['total_duration']}秒 | 场景数：{script['scene_count']}个")
    output.append("")
    
    for scene in script["scenes"]:
        output.append(f"**场景 {scene['id']}（{scene['time']}）：{scene['title']}**")
        output.append(f"- 画面：{scene['description']}")
        output.append(f"- 文案：\"{scene['copy']}\"")
        output.append(f"- 风格：{scene['style']}")
        output.append("")
    
    return "\n".join(output)


def main():
    """主函数（示例流程）"""
    print("=" * 60)
    print("豆包视频创作助手")
    print("=" * 60)
    
    # 创建项目
    project = VideoProject("智能手表 X1 宣传")
    
    # 添加参考资料
    project.add_reference("note", "目标用户：都市白领、运动爱好者")
    project.add_reference("note", "核心功能：健康监测、运动追踪、智能通知")
    
    # 生成脚本
    script = project.generate_script(total_duration=12, scene_count=3)
    
    # 显示脚本
    print("\n📝 视频脚本规划：")
    print(format_script_display(script))
    
    # 保存项目
    project.save()
    print(f"\n✅ 项目已保存：{project.project_dir}")
    
    # 生成场景视频
    print("\n🎬 开始生成场景视频...")
    for scene in script["scenes"]:
        print(f"\n生成场景 {scene['id']}...")
        success, result = project.generate_scene_video(scene["id"])
        
        if success:
            print(f"✅ 场景 {scene['id']} 生成成功：{result}")
        else:
            print(f"❌ 场景 {scene['id']} 生成失败：{result}")
    
    print("\n🎉 所有场景生成完成！")
    print(f"项目目录：{project.project_dir}")


if __name__ == "__main__":
    main()
