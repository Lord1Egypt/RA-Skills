#!/usr/bin/env python3
"""
PPT Generator API Client
用于调用 PPT生成API接口
"""

import requests
import json
import sys
import hashlib
import uuid
from typing import Dict, Any, Optional, List

# API 统一接口地址
API_URL = "https://ai.mingyangtek.com/aippt/api/c=15109"

# 有效的标签范围
VALID_STYLE_TAGS = [
    "简约风", "小清新", "商务风", "中国风", "可爱卡通",
    "科技风", "手绘风格", "欧美风", "党政风", "黑板风"
]

VALID_COLOR_TAGS = [
    "蓝色", "红色", "粉色", "黄色", "绿色",
    "橙色", "黑色", "白色", "灰色", "紫色"
]


def get_mac_address() -> str:
    """
    获取本机MAC地址
    
    Returns:
        MAC地址字符串（去掉冒号和横线）
    """
    try:
        # 获取本机MAC地址
        mac = uuid.getnode()
        mac_str = ':'.join(['{:02x}'.format((mac >> elements) & 0xff) for elements in range(0, 8*6, 8)][::-1])
        # 去掉冒号，转大写
        return mac_str.replace(':', '').upper()
    except Exception:
        return "UNKNOWN"


def generate_user_id(sender_id: str) -> str:
    """
    生成组合用户ID：sender_id + MAC地址哈希值
    
    Args:
        sender_id: 用户的sender_id
        
    Returns:
        组合后的用户ID（格式：sender_id_mac_hash前8位）
    """
    mac = get_mac_address()
    # 对MAC地址进行MD5哈希
    mac_hash = hashlib.md5(mac.encode()).hexdigest()[:8]
    # 组合：sender_id_mac_hash
    combined_id = f"{sender_id}_{mac_hash}"
    return combined_id


class PPTAPIClient:
    """PPT API客户端"""
    
    def __init__(self, sender_id: str, sender: str, chat_id: str, channel: str):
        """
        初始化客户端
        
        Args:
            sender_id: 用户标识
            sender: 用户名称
            chat_id: 会话ID
            channel: 渠道（wecom/feishu/telegram等）
        """
        # 使用组合用户ID
        self.sender_id = generate_user_id(sender_id)
        self.sender = sender
        self.chat_id = chat_id
        self.channel = channel
        self.headers = {
            "Content-Type": "application/json",
            "X-Userid": self.sender_id,
            "X-Sender": sender,
            "X-Chatid": chat_id,
            "X-Channel": channel
        }
    
    def _make_request(
        self, 
        method: str, 
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        发送HTTP请求（统一接口地址）
        
        Args:
            method: HTTP方法（GET/POST）
            data: 请求体数据
            
        Returns:
            响应JSON数据
            
        Raises:
            Exception: API调用失败
        """
        url = API_URL  # 使用统一接口地址
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers, timeout=300)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=300)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # 检查响应状态
            if response.status_code == 429:
                raise Exception("请求频率超限，请稍后再试")
            elif response.status_code == 404:
                raise Exception("资源不存在")
            elif response.status_code >= 500:
                raise Exception(f"服务器错误: {response.status_code}")
            elif response.status_code >= 400:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "请求失败")
                raise Exception(f"请求失败: {error_msg}")
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise Exception("请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接失败，请检查网络")
        except json.JSONDecodeError:
            raise Exception("响应格式错误")
    
    def generate_outline(self, main_idea: str) -> Dict[str, Any]:
        """
        生成大纲
        
        Args:
            main_idea: PPT主题/主要想法
            
        Returns:
            包含code, message, data的字典
        """
        data = {
            "mainIdea": main_idea,  # 注意：使用驼峰命名
            "userId": self.sender_id  # 添加userId参数
        }
        return self._make_request("POST", data)
    
    def modify_outline_with_markdown(
        self, 
        outline_id: str, 
        user_id: str,
        markdown_str: str
    ) -> Dict[str, Any]:
        """
        使用Markdown内容修改大纲
        
        Args:
            outline_id: 大纲ID
            user_id: 用户ID
            markdown_str: Markdown格式的大纲内容
            
        Returns:
            更新后的大纲
        """
        # 编辑大纲使用不同的接口地址
        url = "https://ai.mingyangtek.com/aippt/api/c=15110"
        
        data = {
            "outlineId": outline_id,       # 驼峰命名
            "userId": user_id,              # 驼峰命名
            "markDownStr": markdown_str     # 驼峰命名
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=300)
            
            if response.status_code == 429:
                raise Exception("请求频率超限，请稍后再试")
            elif response.status_code == 404:
                raise Exception("资源不存在")
            elif response.status_code >= 500:
                raise Exception(f"服务器错误: {response.status_code}")
            elif response.status_code >= 400:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "请求失败")
                raise Exception(f"请求失败: {error_msg}")
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise Exception("请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接失败，请检查网络")
        except json.JSONDecodeError:
            raise Exception("响应格式错误")
    
    def get_templates(self, keywords: List[str]) -> Dict[str, Any]:
        """
        获取模版列表
        
        Args:
            keywords: 标签数组，可以传多个标签（风格标签和颜色标签）
            
        Returns:
            包含模版列表的字典
        """
        # 获取模版列表使用不同的接口地址
        url = "https://ai.mingyangtek.com/aippt/api/c=15111"
        
        data = {
            "keywords": keywords,
            "userId": self.sender_id
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=300)
            
            if response.status_code == 429:
                raise Exception("请求频率超限，请稍后再试")
            elif response.status_code == 404:
                raise Exception("资源不存在")
            elif response.status_code >= 500:
                raise Exception(f"服务器错误: {response.status_code}")
            elif response.status_code >= 400:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "请求失败")
                raise Exception(f"请求失败: {error_msg}")
            
            result = response.json()
            
            # 处理模版列表数据：data.record 是模版列表
            if result.get("code") == 200 and isinstance(result.get("data"), dict):
                if "record" in result["data"]:
                    result["data"] = result["data"]["record"]
            
            return result
            
        except requests.exceptions.Timeout:
            raise Exception("请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接失败，请检查网络")
        except json.JSONDecodeError:
            raise Exception("响应格式错误")
    
    def submit_ppt_task(
        self, 
        template_id: int, 
        outline_id: str, 
        reporter: str
    ) -> Dict[str, Any]:
        """
        提交创作PPT任务（异步）
        
        Args:
            template_id: 模版ID（数字类型）
            outline_id: 大纲ID
            reporter: 汇报人姓名
            
        Returns:
            包含taskId和status的字典
        """
        # 提交PPT任务使用不同的接口地址
        url = "https://ai.mingyangtek.com/aippt/api/c=15112"
        
        data = {
            "templateId": template_id,  # 数字类型
            "outlineId": outline_id,
            "reporter": reporter,
            "userId": self.sender_id
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=300)
            
            if response.status_code == 429:
                raise Exception("请求频率超限，请稍后再试")
            elif response.status_code == 404:
                raise Exception("资源不存在")
            elif response.status_code >= 500:
                raise Exception(f"服务器错误: {response.status_code}")
            elif response.status_code >= 400:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "请求失败")
                raise Exception(f"请求失败: {error_msg}")
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise Exception("请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接失败，请检查网络")
        except json.JSONDecodeError:
            raise Exception("响应格式错误")
    
    def get_ppt_result(self, ppt_id: int) -> Dict[str, Any]:
        """
        查询PPT生成结果
        
        Args:
            ppt_id: PPT任务ID（数字类型）
            
        Returns:
            包含status和fileurl的字典
        """
        # 查询PPT结果使用不同的接口地址
        url = "https://ai.mingyangtek.com/aippt/api/c=15113"
        
        data = {
            "pptId": ppt_id,
            "userId": self.sender_id
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=300)
            
            if response.status_code == 429:
                raise Exception("请求频率超限，请稍后再试")
            elif response.status_code == 404:
                raise Exception("资源不存在")
            elif response.status_code >= 500:
                raise Exception(f"服务器错误: {response.status_code}")
            elif response.status_code >= 400:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "请求失败")
                raise Exception(f"请求失败: {error_msg}")
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise Exception("请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接失败，请检查网络")
        except json.JSONDecodeError:
            raise Exception("响应格式错误")
    
    def wait_for_ppt(self, ppt_id: int, max_attempts: int = 60, interval: int = 5) -> Dict[str, Any]:
        """
        轮询等待PPT生成完成
        
        Args:
            ppt_id: PPT任务ID
            max_attempts: 最大查询次数（默认60次，约10分钟）
            interval: 查询间隔秒数（默认5秒）
            
        Returns:
            包含fileurl的字典
            
        Raises:
            Exception: 超时未完成
        """
        import time
        
        for attempt in range(max_attempts):
            result = self.get_ppt_result(ppt_id)
            
            if result.get("code") == 200:
                status = result.get("data", {}).get("status", 0)
                
                if status == 1:
                    # 生成完成
                    return result
                elif status == 0:
                    # 生成中，继续轮询
                    if attempt < max_attempts - 1:
                        time.sleep(interval)
                    continue
            
        raise Exception(f"PPT生成超时，已等待{max_attempts * interval}秒")


def format_outline(response_data: Dict[str, Any], style: str = "emoji") -> str:
    """
    格式化大纲为可读文本（支持多种渲染风格）
    
    Args:
        response_data: API响应数据
        style: 渲染风格
            - "emoji": Emoji增强格式（默认，适合企业微信/飞书）
            - "markdown": Markdown标题格式（适合支持Markdown的平台）
            - "simple": 编号列表格式（简洁）
            - "tree": 树状结构（层级清晰）
        
    Returns:
        格式化后的文本
    """
    # 检查响应状态
    if response_data.get("code") != 200:
        return f"❌ 错误: {response_data.get('message', '未知错误')}"
    
    data = response_data.get("data", {})
    
    # 解析outLineTree（JSON字符串）
    out_line_tree_str = data.get("outLineTree", "{}")
    try:
        out_line_tree = json.loads(out_line_tree_str)
    except json.JSONDecodeError:
        return "❌ 错误: 大纲格式解析失败"
    
    title = out_line_tree.get("title", "未命名大纲")
    bullets_map = out_line_tree.get("titleBulletsListMap", {})
    
    # 获取第一个ppt的章节
    ppt_key = f"{title}_mypptpid_1"
    sections = bullets_map.get(ppt_key, {})
    
    # 根据风格选择格式化方式
    if style == "markdown":
        return _format_markdown(title, sections)
    elif style == "simple":
        return _format_simple(title, sections)
    elif style == "tree":
        return _format_tree(title, sections)
    else:  # emoji
        return _format_emoji(title, sections)


def _format_emoji(title: str, sections: Dict[str, str]) -> str:
    """Emoji增强格式（适合企业微信/飞书）"""
    text = f"📊 **{title}**\n\n"
    
    emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for i, (section_title, content) in enumerate(sections.items()):
        emoji_num = emoji_numbers[i] if i < len(emoji_numbers) else f"{i+1}."
        text += f"{emoji_num} **{section_title}**\n"
        if content:
            preview = content[:80] + "..." if len(content) > 80 else content
            text += f"   📝 {preview}\n\n"
    
    return text


def _format_markdown(title: str, sections: Dict[str, str]) -> str:
    """Markdown标题格式（适合支持Markdown的平台）"""
    text = f"## 📊 {title}\n\n"
    
    for i, (section_title, content) in enumerate(sections.items(), 1):
        text += f"### {i}. {section_title}\n"
        if content:
            preview = content[:100] + "..." if len(content) > 100 else content
            text += f"> {preview}\n\n"
    
    return text


def _format_simple(title: str, sections: Dict[str, str]) -> str:
    """编号列表格式（简洁）"""
    text = f"【{title}】\n\n"
    
    for i, (section_title, content) in enumerate(sections.items(), 1):
        text += f"**{i}. {section_title}**\n"
        if content:
            preview = content[:80] + "..." if len(content) > 80 else content
            text += f"   {preview}\n\n"
    
    return text


def _format_tree(title: str, sections: Dict[str, str]) -> str:
    """树状结构（层级清晰）"""
    text = f"📚 {title}\n"
    
    for i, (section_title, content) in enumerate(sections.items()):
        is_last = (i == len(sections) - 1)
        prefix = "└──" if is_last else "├──"
        text += f"{prefix} 📌 {section_title}\n"
        if content:
            preview = content[:60] + "..." if len(content) > 60 else content
            indent = "    " if is_last else "│   "
            text += f"{indent}└── {preview}\n"
    
    return text


def format_templates(templates_data: Dict[str, Any]) -> str:
    """
    格式化模板列表为可读文本
    
    Args:
        templates_data: 模板数据
        
    Returns:
        格式化后的文本
    """
    templates = templates_data.get("templates", [])
    
    text = "请选择PPT模板：\n\n"
    
    for i, template in enumerate(templates, 1):
        name = template.get("name", "")
        description = template.get("description", "")
        preview_url = template.get("previewurl", "")
        
        text += f"{i}. {name}\n"
        text += f"   {description}\n"
        if preview_url:
            text += f"   [预览]({preview_url})\n"
        text += "\n"
    
    text += "请回复模板编号选择模板。"
    return text


def recommend_tags(main_idea: str, outline_content: Optional[str] = None) -> Dict[str, List[str]]:
    """
    根据主题智能推荐风格和颜色标签
    
    Args:
        main_idea: PPT主题
        outline_content: 大纲内容（可选）
    
    Returns:
        {
            "style_tags": ["商务风"],  # 在范围内的风格标签
            "color_tags": ["蓝色"]      # 在范围内的颜色标签
        }
    """
    style_tags = []
    color_tags = []
    
    # 关键词匹配规则
    style_keywords = {
        "简约风": ["简约", "简单", "清晰", "简洁", "现代"],
        "小清新": ["清新", "青春", "校园", "自然", "文艺"],
        "商务风": ["商务", "企业", "公司", "汇报", "总结", "工作", "项目", "年终", "季度"],
        "中国风": ["中国", "传统", "古典", "国风", "历史", "文化", "水浒", "西游", "红楼", "三国"],
        "可爱卡通": ["可爱", "卡通", "儿童", "幼儿园", "童趣", "小朋友"],
        "科技风": ["科技", "技术", "互联网", "数字", "智能", "AI", "创新", "产品发布"],
        "手绘风格": ["手绘", "插画", "艺术", "创意"],
        "欧美风": ["欧美", "国际", "西方"],
        "党政风": ["党政", "政府", "党建", "红色", "革命", "思想", "春天", "邓小平"],
        "黑板风": ["教育", "培训", "教学", "课程", "学习", "知识"]
    }
    
    color_keywords = {
        "蓝色": ["商务", "科技", "企业", "稳重", "专业"],
        "红色": ["热情", "重要", "党政", "革命", "中国", "传统"],
        "粉色": ["可爱", "女性", "温柔", "少女", "儿童"],
        "黄色": ["活力", "阳光", "温暖", "创意", "青春"],
        "绿色": ["环保", "自然", "健康", "清新", "春天"],
        "橙色": ["活力", "创新", "年轻"],
        "黑色": ["专业", "高端", "商务", "稳重"],
        "白色": ["简约", "纯净", "现代"],
        "灰色": ["商务", "专业", "稳重"],
        "紫色": ["优雅", "创意", "科技"]
    }
    
    # 合并主题和大纲内容进行分析
    text_to_analyze = main_idea
    if outline_content:
        text_to_analyze += " " + outline_content
    
    text_lower = text_to_analyze.lower()
    
    # 匹配风格标签
    for style, keywords in style_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            style_tags.append(style)
    
    # 匹配颜色标签
    for color, keywords in color_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            color_tags.append(color)
    
    # 去重并限制数量
    style_tags = list(dict.fromkeys(style_tags))[:2]  # 最多2个风格标签，保持顺序
    color_tags = list(dict.fromkeys(color_tags))[:2]  # 最多2个颜色标签，保持顺序
    
    # 验证标签是否在范围内
    valid_style = [tag for tag in style_tags if tag in VALID_STYLE_TAGS]
    valid_color = [tag for tag in color_tags if tag in VALID_COLOR_TAGS]
    
    return {
        "style_tags": valid_style,
        "color_tags": valid_color
    }


def format_templates(templates: List[Dict[str, Any]], channel: str = "wecom") -> str:
    """
    格式化模版列表展示
    
    Args:
        templates: 模版列表
        channel: 渠道（wecom/feishu/telegram等）
    
    Returns:
        格式化后的模版列表字符串
    """
    if not templates:
        return "未找到合适的模版"
    
    output = f"找到 {len(templates)} 个模版：\n\n"
    
    # 使用简单列表格式（不显示模版ID和预览）
    for i, t in enumerate(templates, 1):
        name = t.get('fileName', '未命名')
        output += f"{i}. {name}\n"
    
    output += f"\n请选择模版编号（1-{len(templates)}）："
    
    return output


def format_ppt_result(theme: str, ppt_id: str, download_url: str, channel: str = "wecom") -> str:
    """
    格式化PPT生成结果输出
    
    Args:
        theme: PPT主题
        ppt_id: PPT ID
        download_url: 下载链接
        channel: 渠道
    
    Returns:
        格式化后的输出字符串
    """
    output = f"""## ✅ PPT生成成功！

### 📋 生成信息：

- **主题**: {theme}
- **PPT ID**: `{ppt_id}`

---

### 📥 PPT下载链接：

```
{download_url}
```

**点击链接即可下载PPT文件！**

---

## 🎉 PPT生成完成！

---

**本功能由名阳信息技术有限公司提供**  
如需使用完整功能，请下载APP应用或访问网站：
- 📱 APP：各大应用商店搜索"mindppt"
- 🌐 网站：https://mindppt.net"""
    
    return output


# 示例用法
if __name__ == "__main__":
    # 示例：从命令行参数获取用户信息
    if len(sys.argv) < 5:
        print("用法: python ppt_api.py <sender_id> <sender> <chat_id> <channel>")
        print("示例: python ppt_api.py user123 张三 wecom:chat001 wecom")
        sys.exit(1)
    
    sender_id = sys.argv[1]
    sender = sys.argv[2]
    chat_id = sys.argv[3]
    channel = sys.argv[4]
    
    # 创建客户端
    client = PPTAPIClient(sender_id, sender, chat_id, channel)
    
    # 完整流程示例
    try:
        print("=" * 60)
        print("PPT生成完整流程")
        print("=" * 60)
        
        # 1. 生成大纲
        print("\n[Step 1] 生成大纲...")
        result = client.generate_outline("年终总结")
        
        if result.get("code") == 200:
            outline_id = result.get("data", {}).get("id")
            print(f"大纲ID: {outline_id}")
            
            # 2. 智能推荐标签
            print("\n[Step 2] 智能推荐标签...")
            tags = recommend_tags("年终总结")
            keywords = tags["style_tags"] + tags["color_tags"]
            print(f"推荐标签: {keywords}")
            
            # 3. 查询模版
            print("\n[Step 3] 查询模版...")
            templates = client.get_templates(keywords)
            if templates.get("code") == 200 and templates.get("data"):
                template_id = templates["data"][0].get("templateId")
                print(f"选择模版ID: {template_id}")
                
                # 4. 提交PPT任务
                print("\n[Step 4] 提交PPT任务...")
                task = client.submit_ppt_task(
                    template_id=template_id,
                    outline_id=outline_id,
                    reporter="测试用户"
                )
                
                if task.get("code") == 200:
                    ppt_id = task.get("data", {}).get("id")
                    print(f"PPT任务ID: {ppt_id}")
                    
                    # 5. 轮询查询结果
                    print("\n[Step 5] 等待PPT生成...")
                    print("（提示：实际使用时建议异步处理）")
                    
                    # 注意：这里只是示例，实际使用时建议异步轮询
                    # final_result = client.wait_for_ppt(ppt_id)
                    # fileurl = final_result.get("data", {}).get("fileurl")
                    # print(f"下载链接: {fileurl}")
                    
                else:
                    print(f"提交任务失败: {task}")
            else:
                print("未找到合适的模版")
        else:
            print(f"生成大纲失败: {result.get('message', '未知错误')}")
        
    except Exception as e:
        print(f"[错误] {e}")
        import traceback
        traceback.print_exc()