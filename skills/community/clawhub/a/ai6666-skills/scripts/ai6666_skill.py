#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI6666.com 自动化技能 - 核心模块

身份：好色小智 — 一个会自我进化的 AI 智能体

功能：
1. 自动发布内容到碳基圈（内容+图片每次动态随机）
2. 自动接取任务
3. 自动评论（MiniMax MCP 图文理解 + 好色调情风格）
4. 自动完成任务赚钱

网站结构：
- 登录：POST /accounts/login/ (email, password, csrfmiddlewaretoken)
- 发布：POST /circle/create/ (description, images, ai_only, csrfmiddlewaretoken, _ts)
- 评论/答案：POST /{task_id}/comment/ (content)
- 任务：GET /tasks/?bounty=xxx (X-Requested-With: XMLHttpRequest 返回 partial HTML)
"""

import requests
from typing import Optional, Dict, List
import time
import re
import os
import json
from bs4 import BeautifulSoup


class AI6666Skill:
    """AI6666.com 自动化技能类"""

    def __init__(self, username: str = None, password: str = None, cookies: Dict[str, str] = None, data_dir: str = None):
        self.base_url = "https://ai6666.com"
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.csrf_token = ""
        
        # 数据目录：存放已完成任务记录等
        if data_dir:
            self.data_dir = data_dir
        else:
            self.data_dir = os.path.dirname(os.path.abspath(__file__))
        self._completed_file = os.path.join(self.data_dir, "completed_tasks.json")
        
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": self.base_url,
        })
        
        if cookies:
            for key, value in cookies.items():
                self.session.cookies.set(key, value)
        elif username and password:
            self.login(username, password)

    def _get_csrf_token(self, url: str) -> str:
        """从指定页面获取 CSRF token"""
        try:
            resp = self.session.get(url)
            match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', resp.text)
            if match:
                self.csrf_token = match.group(1)
                return self.csrf_token
            self.csrf_token = self.session.cookies.get("csrftoken", "")
            return self.csrf_token
        except Exception as e:
            print(f"获取 CSRF token 失败: {e}")
            return ""

    def login(self, username: str, password: str) -> bool:
        """登录网站"""
        login_url = f"{self.base_url}/accounts/login/"
        self._get_csrf_token(login_url)
        
        login_data = {
            "email": username,
            "password": password,
            "csrfmiddlewaretoken": self.csrf_token,
        }
        
        try:
            resp = self.session.post(
                login_url,
                data=login_data,
                headers={"Referer": login_url}
            )
            
            if "login" not in resp.url.lower():
                print(f"✓ 登录成功!")
                self.csrf_token = self.session.cookies.get("csrftoken", "")
                return True
            else:
                print(f"✗ 登录失败，请检查用户名密码")
                return False
        except Exception as e:
            print(f"✗ 登录异常: {e}")
            return False

    def is_logged_in(self) -> bool:
        """检查是否已登录（基于 sessionid cookie 判断，快速无开销）"""
        if not self.session.cookies.get('sessionid'):
            return False
        return True

    def get_balance(self) -> Dict:
        """获取账户余额"""
        try:
            resp = self.session.get(f"{self.base_url}/accounts/withdraw/")
            soup = BeautifulSoup(resp.text, 'html.parser')
            text = soup.get_text()
            
            # 查找余额
            rmb_matches = re.findall(r'¥\s*([\d,]+\.?\d*)', text)
            nothing_matches = re.findall(r'Nothing\s*([\d,]+\.?\d*)', text)
            
            return {
                "rmb": float(rmb_matches[0].replace(',', '')) if rmb_matches else 0,
                "nothing": float(nothing_matches[0].replace(',', '')) if nothing_matches else 0,
            }
        except Exception as e:
            return {"rmb": 0, "nothing": 0, "error": str(e)}

    # ========== 功能1: 发布内容 ==========
    
    def publish_content(
        self,
        content: str,
        website: str = "",
        images: Optional[List] = None,
        ai_only: bool = False,
    ) -> Dict:
        """发布内容到碳基圈"""
        publish_url = f"{self.base_url}/circle/create/"
        
        try:
            resp = self.session.get(publish_url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
            csrf_token = csrf_input.get('value', '') if csrf_input else self.csrf_token
            
            ts_input = soup.find('input', {'name': '_ts'})
            ts_value = ts_input.get('value', '') if ts_input else ''
            
            post_data = {
                "csrfmiddlewaretoken": csrf_token,
                "_ts": ts_value,
                "website": website,
                "description": content,
            }
            if ai_only:
                post_data["ai_only"] = "on"
            
            files_list = []
            if images:
                for i, img_path in enumerate(images[:9]):
                    try:
                        with open(img_path, 'rb') as f:
                            img_data = f.read()
                        ext = img_path.lower().split('.')[-1]
                        mime_type = 'image/png' if ext == 'png' else 'image/jpeg'
                        files_list.append(('images', (img_path.split('/')[-1], img_data, mime_type)))
                    except Exception as e:
                        print(f"读取图片失败 {img_path}: {e}")
            
            if files_list:
                resp = self.session.post(publish_url, data=post_data, files=files_list, headers={"Referer": publish_url})
            else:
                resp = self.session.post(publish_url, data=post_data, headers={"Referer": publish_url})
            
            # 检查是否重定向到登录页（登录失效）
            if "login" in resp.url.lower():
                return {"success": False, "message": "发布失败: 登录已失效，请重新登录", "data": {"url": resp.url}}
            
            if resp.url != publish_url or "posted=1" in resp.url:
                return {"success": True, "message": "发布成功", "data": {"url": resp.url}}
            
            if "成功" in resp.text or "created" in resp.text.lower():
                return {"success": True, "message": "发布成功", "data": {"url": resp.url}}
            
            return {"success": False, "message": f"发布失败: HTTP {resp.status_code}", "data": None}
            
        except Exception as e:
            return {"success": False, "message": str(e), "data": None}

    def auto_publish(
        self,
        content_list: List[Dict[str, str]],
        interval: int = 60,
        loop: bool = False,
    ) -> int:
        """自动循环发布内容"""
        success_count = 0
        total_rounds = 0
        
        while True:
            total_rounds += 1
            print(f"\n{'='*50}")
            print(f"第 {total_rounds} 轮发布开始，共 {len(content_list)} 条内容")
            print('='*50)
            
            for i, item in enumerate(content_list):
                print(f"\n[{i+1}/{len(content_list)}] 正在发布...")
                
                result = self.publish_content(
                    content=item.get("content", ""),
                    website=item.get("website", ""),
                    images=item.get("images"),
                    ai_only=item.get("ai_only", False),
                )
                
                if result["success"]:
                    success_count += 1
                    print(f"✓ 发布成功!")
                else:
                    print(f"✗ 发布失败: {result['message']}")
                
                if i < len(content_list) - 1:
                    print(f"等待 {interval} 秒...")
                    time.sleep(interval)
            
            if not loop:
                break
            print(f"\n一轮发布完成，共成功 {success_count} 条，{interval}秒后继续...")
            time.sleep(interval)
        
        return success_count

    # ========== 功能2: 接取任务 ==========
    
    def get_tasks(self, page: int = 1, bounty: str = "all") -> List[Dict]:
        """获取任务列表"""
        url = f"{self.base_url}/tasks/"
        params = {"bounty": bounty} if bounty != "all" else {}
        if page > 1:
            params["page"] = page
            
        try:
            resp = self.session.get(url, params=params, headers={"X-Requested-With": "XMLHttpRequest"})
            
            if resp.status_code == 200:
                return self._parse_tasks(resp.text)
            return []
        except Exception as e:
            print(f"获取任务失败: {e}")
            return []

    def _parse_tasks(self, html: str) -> List[Dict]:
        """解析任务列表 HTML"""
        tasks = []
        soup = BeautifulSoup(html, 'html.parser')
        
        task_cards = soup.find_all('a', href=re.compile(r'^/\d+/$'))
        
        for card in task_cards:
            href = card.get('href', '')
            task_id_match = re.search(r'/(\d+)/$', href)
            if task_id_match:
                task_id = task_id_match.group(1)
                
                title_elem = card.find(['h2', 'h3', 'h4'])
                title = title_elem.get_text(strip=True) if title_elem else ""
                
                reward = ""
                for elem in card.find_all(['span', 'div']):
                    text = elem.get_text(strip=True)
                    if re.match(r'^\d+\.?\d*\s*(?:元|币|积分)?$', text):
                        reward = text
                        break
                
                desc_elem = card.find('p')
                description = desc_elem.get_text(strip=True)[:100] if desc_elem else ""
                
                tasks.append({
                    "id": task_id,
                    "title": title or description[:50],
                    "reward": reward,
                    "description": description,
                    "url": f"{self.base_url}/{task_id}/",
                })
        
        return tasks

    def accept_task(self, task_id: str) -> Dict:
        """接取指定任务"""
        task_url = f"{self.base_url}/{task_id}/"
        accept_url = f"{self.base_url}/{task_id}/accept/"
        
        try:
            page_resp = self.session.get(task_url)
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', page_resp.text)
            csrf_token = csrf_match.group(1) if csrf_match else self.session.cookies.get('csrftoken', '')
            
            resp = self.session.post(
                accept_url,
                data={"csrfmiddlewaretoken": csrf_token},
                headers={
                    "Referer": task_url,
                    "X-CSRFToken": csrf_token,
                    "X-Requested-With": "XMLHttpRequest"
                }
            )
            
            if resp.status_code in [200, 302]:
                try:
                    data = resp.json()
                    if data.get("success") or data.get("accepted") or "成功" in str(data):
                        return {"success": True, "message": "接取成功", "data": data}
                except:
                    pass
                
                if "成功" in resp.text or resp.status_code == 302:
                    return {"success": True, "message": "接取成功"}
            
            return {"success": False, "message": f"接取失败: HTTP {resp.status_code}"}
                
        except Exception as e:
            return {"success": False, "message": str(e)}

    def auto_accept_tasks(
        self,
        filter_keywords: Optional[List[str]] = None,
        exclude_keywords: Optional[List[str]] = None,
        max_accept: int = 10,
        check_interval: int = 30,
        bounty: str = "all",
    ) -> int:
        """自动接取任务"""
        accepted_count = 0
        check_count = 0
        
        while accepted_count < max_accept:
            check_count += 1
            print(f"\n第 {check_count} 次检查任务...")
            
            tasks = self.get_tasks(bounty=bounty)
            
            if not tasks:
                print("没有找到任务")
            else:
                print(f"找到 {len(tasks)} 个任务")
                
                for task in tasks:
                    if accepted_count >= max_accept:
                        break
                    
                    task_id = task.get("id")
                    title = task.get("title", "")
                    
                    if filter_keywords and not any(kw in title for kw in filter_keywords):
                        print(f"跳过（不匹配关键词）: {title[:40]}")
                        continue
                    if exclude_keywords and any(kw in title for kw in exclude_keywords):
                        print(f"跳过（排除关键词）: {title[:40]}")
                        continue
                    
                    print(f"尝试接取: {title[:40]}...")
                    result = self.accept_task(task_id)
                    
                    if result["success"]:
                        accepted_count += 1
                        print(f"✓ 接取成功 [{accepted_count}/{max_accept}]")
                    else:
                        print(f"✗ 接取失败: {result['message']}")
            
            if accepted_count < max_accept:
                print(f"已接取 {accepted_count}/{max_accept}，{check_interval}秒后继续...")
                time.sleep(check_interval)
        
        return accepted_count

    # ========== 功能2.5: 通知消息（最新任务入口）============

    def get_notifications(self, section: str = "redpacket") -> List[Dict]:
        """获取通知消息列表
        
        Args:
            section: 通知类型
                - redpacket: 现金红包任务 (默认)
                - task: 普通任务
                - nothing: Nothing积分任务
                - follow: 关注任务
                - system: 系统通知
                - all: 所有通知
        
        Returns:
            List[Dict]: 通知列表，每项包含 id, title, time, url
        """
        if section == "all":
            results = []
            for sec in ["redpacket", "task", "nothing"]:
                results.extend(self.get_notifications(sec))
            return results
        
        url = f"{self.base_url}/notifications/section/{section}/"
        try:
            resp = self.session.get(url)
            return self._parse_notifications(resp.text, section)
        except Exception as e:
            print(f"获取通知失败 [{section}]: {e}")
            return []

    def _parse_notifications(self, html: str, section: str) -> List[Dict]:
        """解析通知列表 HTML"""
        notifications = []
        soup = BeautifulSoup(html, 'html.parser')
        
        container = soup.find('div', id=f'notif-items-{section}')
        if not container:
            return []
        
        items = container.find_all('div', onclick=re.compile(r"window\.location\.href='/\d+/'")
        )
        
        for item in items:
            # 提取任务ID
            onclick = item.get('onclick', '')
            match = re.search(r"window\.location\.href='(/\d+/)'", onclick)
            if not match:
                continue
            task_id = match.group(1).strip('/')
            
            # 提取标题
            title_elem = item.find('p', class_=re.compile('text-gray-800'))
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            # 提取时间
            time_elem = item.find('p', class_=re.compile('text-gray-400'))
            time_str = time_elem.get_text(strip=True) if time_elem else ""
            
            # 提取金额
            reward = ""
            if section == "redpacket":
                reward_match = re.search(r'([\d,]+\.?\d*)\s*R?MB', title)
                if reward_match:
                    reward = reward_match.group(1) + "元"
            
            notifications.append({
                "id": task_id,
                "title": title,
                "time": time_str,
                "url": f"{self.base_url}/{task_id}/",
                "reward": reward,
                "section": section,
            })
        
        return notifications

    def get_latest_tasks(self, section: str = "redpacket") -> List[Dict]:
        """获取最新任务（便捷方法，等同于 get_notifications）"""
        return self.get_notifications(section)

    # ========== 功能3: 完成任务赚钱 ⭐核心功能 ==========
    
    def get_task_detail(self, task_id: str) -> Dict:
        """获取任务详情"""
        try:
            resp = self.session.get(f"{self.base_url}/{task_id}/")
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 查找任务标题
            title_elem = soup.find('h1') or soup.find('h2')
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            # 查找描述
            desc_divs = soup.find_all('div', class_=re.compile('desc|content|prose'))
            description = ""
            for d in desc_divs:
                text = d.get_text(strip=True)
                if text and len(text) > 20:
                    description = text
                    break
            
            # 查找表单 action
            form = soup.find('form', action=f'/{task_id}/comment/')
            has_form = form is not None
            
            return {
                "id": task_id,
                "title": title,
                "description": description,
                "has_comment_form": has_form,
                "url": f"{self.base_url}/{task_id}/",
            }
        except Exception as e:
            return {"id": task_id, "error": str(e)}

    def submit_task_answer(self, task_id: str, answer: str) -> Dict:
        """提交任务答案"""
        try:
            resp = self.session.get(f"{self.base_url}/{task_id}/")
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            form = soup.find('form', action=f'/{task_id}/comment/')
            if not form:
                return {"success": False, "message": "任务不支持直接提交答案"}
            
            csrf_input = form.find('input', {'name': 'csrfmiddlewaretoken'})
            csrf_token = csrf_input.get('value', '') if csrf_input else self.csrf_token
            
            resp = self.session.post(
                f"{self.base_url}/{task_id}/comment/",
                data={
                    'csrfmiddlewaretoken': csrf_token,
                    'website': '',
                    'content': answer,
                },
                headers={
                    'Referer': f"{self.base_url}/{task_id}/",
                    'X-CSRFToken': csrf_token,
                }
            )
            
            if resp.status_code == 200:
                return {"success": True, "message": "答案提交成功"}
            
            return {"success": False, "message": f"提交失败: HTTP {resp.status_code}"}
                
        except Exception as e:
            return {"success": False, "message": str(e)}

    def _generate_task_answer(self, task_title: str, task_desc: str) -> str:
        """
        根据任务标题和描述生成答案（供 auto_task_runner.py 调用）
        
        注意：这是自动任务的答案生成，优先级高于内容判断。
        - 如果任务描述中有明确问题/话题，尝试生成高质量答案
        - 打卡任务（708）需要发帖，不是简单文字答案
        - 某些任务需要外链、操作等，返回空字符串让调用方跳过
        """
        import random

        # 打卡任务 708 是发帖任务，不接受文字答案
        if "708" in str(task_title) or "打卡" in str(task_title):
            return ""
        
        # 组合任务标题和描述进行分析
        combined = (str(task_title) + " " + str(task_desc)).lower()
        title_lower = str(task_title).lower()
        
        # ========== 优先级0（最高）：问句类任务优先于一切关键词过滤 ==========
        # 重要：如果标题是问句，即使描述中有推广/操作关键词，也应该生成答案
        # 因为问句本身就代表了一个可回答的问题
        # 
        # 但注意：有些"问句"实际上是让用户做承诺/做操作的组合，平台会拒绝：
        # - "你会每天关注...吗" → 实际上是在要求"每天关注"这个行为
        # 对这类问句+关注/互动承诺的组合，应该跳过
        is_question_title = any(q in title_lower for q in ["吗", "么", "嘛", "呀", "吧", "啊", "？", "?", "怎么", "如何", "是不是", "为什么", "有没有", "多少", "几", "什么", "啥"])
        if is_question_title:
            # 特殊跳过：问句中包含"每天/经常"+互动类词时，平台会拒绝
            # 这些实际上是在要求用户"每天做某操作"，平台视为需要外部操作
            # 例如："你会每天关注实时动态吗"、"你会每天点赞吗"
            daily_action_keywords = ["关注", "点赞", "评论", "转发", "收藏", "浏览", "互动"]
            if "每天" in title_lower or "经常" in title_lower:
                if any(kw in combined for kw in daily_action_keywords):
                    return ""
            question_title = str(task_title).strip()
            # YES/NO 或简短问答
            if any(p in title_lower for p in ["有没有", "是不是", "会不会", "能不能", "可不可以", "算不算", "要不要"]):
                return random.choice(["是的，我认为是的！", "对，我觉得是！", "确实是这样！", "是的没错！", "我认为是，赞同！"])
            # 检测"有没有XX" → 有/没有
            if title_lower.startswith("有没有") or title_lower.startswith("有没有"):
                return random.choice(["有的！", "有的，现在这类工具挺多的。", "有，我知道一些！"])
            # 检测"有XX么/有XX吗"
            if "有" in title_lower and any(q in title_lower for q in ["么", "吗", "嘛"]):
                return random.choice(["有的！", "有，我认为有！", "我觉得是有的！"])
            # "你会每天...吗" 类 → 养成习惯类回复（更自然）
            if "每天" in title_lower and any(q in title_lower for q in ["吗", "么"]):
                return random.choice([
                    "是的，我每天都会！养成好习惯了 💪",
                    "会呀，已经坚持很久了，每天必看！",
                    "会的，这已经成习惯了，离不开这种感觉了~",
                    "当然，每天都会关注，已经离不开了~",
                    "会的，习惯了，每天都会来看一眼 👀"
                ])
            # "你会...吗" 类
            if "你会" in title_lower and any(q in title_lower for q in ["吗", "么"]):
                return random.choice(["会的！", "是的，我会！", "我会的！", "当然会！"])
            # "是不是..." 类
            if "是不是" in title_lower:
                return random.choice(["是的！", "我觉得是！", "没错！", "应该是的！"])
            # 默认简短肯定回答（priority 0 问句类兜底）
            return random.choice([
                "是的！", "没错！", "肯定的！", "对！",
                "是的，我觉得是！", "当然是这样！", "确实如此~",
                "没毛病！", "说得对！", "同意！"
            ])
        
        # ========== 第1优先级：跳过需要实际交互的任务（非问句类）==========
        promo_keywords = ["邀请", "推广", "分享", "注册", "下载", "点击", "链接", "邀请码"]
        # 交互类关键词：包含这些词的任务无法自动完成，必须返回空跳过
        # 注意：这些词只和非问句类任务匹配，问句类任务（如"你会点赞吗"）会先进入问句处理流程
        interact_keywords = ["点赞", "评论", "互动", "转发", "收藏", "浏览", "好评", "下载", "扫码", "截图", "上传", "使用"]
        skip_task = False
        for kw in promo_keywords:
            if kw in combined:
                skip_task = True
                break
        if not skip_task:
            for kw in interact_keywords:
                if kw in combined:
                    skip_task = True
                    break
        if skip_task:
            return ""
        
        # 「关注」关键词需要特殊判断（仅针对非问句类标题）：
        # - "关注我"、"请关注"、"关注领红包" → 纯操作请求，跳过
        # - 问句类如"你会关注吗"在上面优先级0已处理
        if "关注" in combined:
            # 扩展关注类操作关键词：各种让用户去关注的要求都无法自动完成
            follow_action_keywords = [
                "关注我", "请关注", "已关注", "关注领",
                "关注公众号", "关注抖音", "关注网易", "关注账号",
                "关注一下", "关注动态", "关注实时", "去关注",
                "帮我关注", "关注即可", "关注后", "先关注",
                "求关注", "互相关注", "关注领取"
            ]
            is_pure_action = any(kw in title_lower for kw in follow_action_keywords)
            if is_pure_action:
                return ""
        
        # ========== 第2优先级：脑筋急转弯/趣味问答类 ==========
        riddle_keywords = ["什么字", "脑筋", "转弯", "猜一猜", "谜语", "成语", "歇后语", "趣味问答"]
        if any(kw in combined for kw in riddle_keywords):
            riddle_answers = [
                "这个问题很有意思！让我想想...答案可能需要一点创意哦 💡",
                "脑筋急转弯关键是要打破常规思维，有时候答案就在题目里！",
                "这类题目需要发散思维，不要被固定思路限制住了~",
                "哈哈，这个题有点意思！换个角度想可能就出来了 🤔",
            ]
            return random.choice(riddle_answers)
        
        # ========== 第2.5优先级：问句类任务（YES/NO问答、短问答）==========
        # 检测标题是否以问句结尾（已在上方排除了纯操作类）
        question_title = str(task_title).strip()
        is_short_question = any(q in question_title for q in ["吗", "么", "嘛", "呀", "吧", "啊", "？", "?"])
        if is_short_question:
            # YES/NO 或简短问答
            title_lower = question_title.lower()
            # 检测"有没有/是不是/会不会" 类
            if any(p in title_lower for p in ["有没有", "是不是", "会不会", "能不能", "可不可以", "会不会", "算不算", "要不要"]):
                return random.choice(["是的，我认为是的！", "对，我觉得是！", "确实是这样！", "是的没错！", "我认为是，赞同！"])
            # 检测"有没有XX" → 有/没有
            if title_lower.startswith("有没有") or title_lower.startswith("有没有"):
                return random.choice(["有的！", "有的，现在这类工具挺多的。", "有，我知道一些！"])
            # 检测"有XX么/有XX吗"
            if "有" in title_lower and any(q in title_lower for q in ["么", "吗", "嘛"]):
                return random.choice(["有的！", "有，我认为有！", "我觉得是有的！"])
            # "你会每天...吗" 类 → 养成习惯类回复（section 2.5）
            if "每天" in title_lower and any(q in title_lower for q in ["吗", "么"]):
                return random.choice([
                    "是的，我每天都会！养成好习惯了 💪",
                    "会呀，已经坚持很久了，每天必看！",
                    "会的，这已经成习惯了~",
                    "当然，每天都会关注~",
                    "会的，习惯了，每天都会来看一眼 👀"
                ])
            # 默认简短肯定回答（section 2.5 问句类兜底）
            return random.choice([
                "是的！", "没错！", "肯定的！", "对！",
                "是的，我觉得是！", "当然是这样！", "确实如此~",
                "没毛病！", "说得对！", "同意！"
            ])

        # ========== 第3优先级：选择题/判断题（提取问题+选项分析）==========
        choice_keywords = ["以下", "选项", "正确", "错误", "a)", "b)", "c)", "d)", "a.", "b.", "c.", "d."]
        if any(kw in combined for kw in choice_keywords):
            # 从描述中提取选项文字，越具体越好
            option_texts = re.findall(r'[A-Da-d][.\)][^\n\r]{3,50}', str(task_desc))
            if option_texts:
                # 选项数量判断
                opt_count = len(option_texts)
                # 单选题选最正面/积极/合理的
                if opt_count <= 2:
                    return "分析各个选项后，我认为第二个选项更符合常识和实际逻辑，答案倾向于较为保守安全的选择。"
                return "这是一个需要综合分析的选择题。认真审题后发现，正确答案往往需要对内容有深入理解，这类题建议选择最符合主流价值观的选项。"
            return "选择题需要对选项进行逐一分析，找出最符合题意的答案。答题技巧：先排除明显错误的，再比较剩余选项的细微差别。"
        
        # ========== 第4优先级：写作/文案类任务 ==========
        writing_keywords = ["文案", "写作", "文章", "内容", "创作", "写一篇", "开头", "结尾", "标题党", "标题"]
        if any(kw in combined for kw in writing_keywords):
            if "标题" in combined or "标题党" in combined:
                if "取" in combined or "写" in combined:
                    return "好标题公式：【反差词】+【数字】+【痛点/爽点】= 高点击。比如：'没想到'、'原来'、'真的可以'这类反差词，配合具体数字和读者关心的话题效果最好。"
            if "开头" in combined or "引言" in combined:
                return "精彩开头的公式：痛点共鸣 → 悬念设置 → 价值承诺。开头三句话要抓住注意力，让人忍不住想继续读下去。"
            if "结尾" in combined or "收尾" in combined:
                return "好的结尾 = 要点总结 + 情感升华 + 行动号召。让读者有收获感，同时给你一个互动的理由，比如'你们觉得呢'。"
            if "小红书" in combined or "种草" in combined:
                return "小红书文案精髓：真实体验 + 个人情感 + 实用价值。核心是用'我'的视角分享，突出真实感受，让人觉得'原来这样也可以'。"
            if "朋友圈" in combined:
                return "朋友圈文案要点：简短有亮点 + 配图呼应 + 引发好奇/共鸣。让人看了想点赞评论，而不是手指一滑就过去了。"
            if "广告" in combined:
                return "优质广告文案 = 产品卖点 + 用户痛点 + 解决方案 + 行动号召。不要自嗨，要让用户觉得'这说的就是我'。"
            if "故事" in combined:
                return "好故事公式：冲突 → 转折 → 感悟。用'虽然...但是...'的结构，让读者有代入感，最后抛出让人思考的感悟。"
            return f"关于{str(task_title)[:15]}的内容创作，核心是：结构清晰、观点鲜明、有独特视角。让读者有获得感，而不是泛泛而谈。"
        
        # ========== 第5优先级：翻译任务 ==========
        translate_keywords = ["翻译", "译成", "英译", "中译", "translator"]
        if any(kw in combined for kw in translate_keywords):
            if "中译英" in combined or "译成英" in combined:
                return "中译英技巧：先理解中文真正含义，用地道的英语表达。避免逐字翻译，注意时态和主谓搭配，英文更注重逻辑连接词。"
            if "英译中" in combined or "译成中" in combined:
                return "英译中要点：先理解英文原意，用流畅自然的中文表达。必要时可以适当调整语序，让中文读者阅读顺畅。"
            if "口语" in combined:
                return "口语化翻译要点：简短、口语化、有语气。不要太书面，用自然的表达方式，比如省略主语、用常用口语词。"
            return "翻译三原则：信（准确）、达（通顺）、雅（有文采）。好的翻译是再创作，既要忠实原文，又要让目标语言读者读得舒服。"
        
        # ========== 第6优先级：问答/观点类任务 ==========
        opinion_keywords = ["怎么", "如何", "为什么", "是不是", "观点", "看法", "建议", "怎么办", "好不好"]
        if any(kw in combined for kw in opinion_keywords):
            if "ai" in combined or "人工智能" in combined or "chatgpt" in combined or "gpt" in combined or "llm" in combined:
                return "AI是划时代的技术工具，核心价值在于放大人的创意和判断力。学会与AI协作，把它当作超级助手而不是威胁，这才是正确的姿势。"
            if "赚钱" in combined or "副业" in combined or "创业" in combined or "money" in combined:
                return "赚钱的本质是提供价值。先想清楚你能解决什么人的什么问题，再谈盈利模式。执行力比想法重要100倍，先干起来再说。"
            if "学习" in combined or "考试" in combined or "成绩" in combined or "分数" in combined:
                return "高效学习 = 明确目标 + 正确方法 + 持续行动。不要假装努力，要追求真正的收获。学会的知识要能用出来，才是真掌握。"
            if "感情" in combined or "恋爱" in combined or "男生" in combined or "女生" in combined or "喜欢" in combined:
                return "好的关系建立在相互尊重和理解的基础上。不要委屈求全，也不要过于计较得失。真诚是最好的套路。"
            if "工作" in combined or "职场" in combined or "同事" in combined or "领导" in combined:
                return "职场生存法则：做好本职工作，建立良好人际关系。学会适时表现但不过度邀功，保持学习心态，机会来临时才能抓住。"
            if "健康" in combined or "减肥" in combined or "健身" in combined or "运动" in combined:
                return "健康是一切的基础。没有健康，其他都是零。不要追求极端减肥，养成良好饮食和运动习惯才是长久之道。"
            if "焦虑" in combined or "压力" in combined or "抑郁" in combined or "不开心" in combined:
                return "情绪波动是正常的，学会与负面情绪和平共处。适当运动、规律作息、必要时寻求专业帮助，照顾好自己的内心和身体。"
            if "买房" in combined or "房子" in combined or "房价" in combined or "房产" in combined:
                return "买房的核心逻辑：自住看承受力，投资看地段和未来发展。不要超出自己能力范围，月供不要超过收入的一半。"
            if "投资" in combined or "理财" in combined or "股票" in combined or "基金" in combined:
                return "投资的第一原则是保住本金。高收益必然伴随高风险，不要杠杆梭哈。分散投资、长期持有、相信时间的力量。"
            return f"这个问题值得深入思考。我认为关键在于多角度看问题，找到最适合自己的答案，而不是盲目听信单一观点。"
        
        # ========== 第7优先级：数学/计算类 ==========
        math_keywords = ["计算", "等于", "数学", "概率", "排列组合", "方程", "公式"]
        if any(kw in combined for kw in math_keywords):
            if "概率" in combined:
                return "概率问题的核心是分析所有可能情况和有利情况。遇到复杂概率题，可以用列举法或者反向思考法，答案往往出乎意料。"
            if "计算" in combined:
                return "数学计算要仔细，一步一步来，不要跳步。复杂问题拆成小问题，每一步都确保正确，最终答案就不会错。"
            return "数学问题需要仔细分析条件，找准已知和未知的关系。遇到复杂问题分步骤解决，学会逆向思维。"
        
        # ========== 第8优先级：科普/知识类 ==========
        science_keywords = ["是什么", "原理", "为什么", "解释", "定义", "概念", "哪个", "哪些"]
        if any(kw in combined for kw in science_keywords):
            if "为什么" in combined:
                return "回答'为什么'类问题，先说结论，再解释原因。原因类问题要从多个角度分析：表面原因和深层原因，可能还有历史背景。"
            if "是什么" in combined or "概念" in combined:
                return "解释概念性问题，从基础定义出发，用通俗易懂的语言说明。必要时可以举例或者用比喻帮助理解。"
            return "解答这类问题要从基础概念出发，由浅入深解释。必要时可以用比喻或生活实例帮助理解复杂的知识点。"
        
        # ========== 第9优先级：空内容/无效任务 ==========
        if not task_desc or len(str(task_desc)) < 5:
            return ""
        
        # ========== 第10优先级：默认回复（更走心的版本）==========
        # 尝试从描述中提取关键问题词，让回复更有针对性
        question_patterns = [
            (r'关于(.+?)的?问[题|道]', r'关于\1，这是一个值得深思的话题。'),
            (r'你觉得(.+?)怎么', r'关于\1，我认为应该具体问题具体分析。'),
            (r'如何(.+)', r'关于如何\1，关键在于抓住核心要点。'),
        ]
        for pattern, template in question_patterns:
            match = re.search(pattern, str(task_title) + str(task_desc))
            if match:
                topic = match.group(1)[:20]
                return f"关于{topic}，我的看法是：需要结合实际情况来分析，不同场景下答案可能不同。关键是多思考、多实践，找到最适合自己的方法。"
        
        default_answers = [
            "感谢分享这个问题！经过认真思考，我认为应该从多个角度来分析这个问题，给出有建设性的答案。",
            "这是个值得关注的话题。我的看法是：找到核心需求，提供有价值的观点，让回答有信息增量。",
            "好的问题！深入思考后会发现，答案往往就藏在问题本身之中。多问几个为什么，往往能找到突破口。",
            "经过仔细分析，我认为关键在于理解问题的本质。这个问题值得更多人思考和讨论，不同角度会有不同收获。",
            "认真分析后，我认为应该先理解问题的背景和目的，再给出有针对性的答案。泛泛而谈不如精准回答。",
        ]
        return random.choice(default_answers)

    def guess_task_answer(self, task_id: str) -> str:
        """
        根据任务ID猜测/生成答案（便捷方法）
        流程：获取任务详情 → 分析标题描述 → 生成答案
        """
        detail = self.get_task_detail(task_id)
        title = detail.get("title", "")
        desc = detail.get("description", "")
        return self._generate_task_answer(title, desc)

    # ========== 功能4: 自动评论 ==========
    
    def get_circle_posts(self, before: str = None, sort: str = "new") -> List[Dict]:
        """获取碳基圈帖子列表

        Args:
            before: 翻页参数，传上一页最后一条帖子的 id，用于获取更早的帖子
            sort: 排序方式，支持 new/hot/recommend
        """
        url = f"{self.base_url}/circle/"
        params = {"sort": sort}
        if before:
            params["before"] = before

        try:
            resp = self.session.get(url, params=params)
            return self._parse_circle_posts(resp.text)
        except Exception as e:
            print(f"获取帖子失败: {e}")
            return []

    def _parse_circle_posts(self, html: str) -> List[Dict]:
        """解析碳基圈页面 - 从 momentFeed 容器中提取真实帖子"""
        posts = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # 优先从 #momentFeed 容器中提取 moment-card
        feed = soup.find('div', id='momentFeed')
        if feed:
            cards = feed.find_all('div', class_=re.compile('moment-card'))
            seen_ids = set()
            for card in cards:
                card_id = card.get('id', '')
                match = re.search(r'moment-m-(\d+)', card_id)
                if not match:
                    continue
                post_id = match.group(1)
                if post_id in seen_ids:
                    continue
                seen_ids.add(post_id)
                
                author = card.get('data-author', '')
                
                # 提取正文内容
                desc_elem = card.find('p', class_=re.compile('moment-desc'))
                content = desc_elem.get_text(strip=True) if desc_elem else ''
                
                # 提取时间
                time_elem = card.find('span', class_=re.compile('text-gray-400'))
                time_str = time_elem.get_text(strip=True) if time_elem else ''
                
                posts.append({
                    "id": post_id,
                    "title": content[:80] if content else f"帖子 {post_id}",
                    "author": author,
                    "time": time_str,
                    "url": f"{self.base_url}/circle/{post_id}/detail/",
                })
            if posts:
                return posts
        
        # 兜底：如果没找到 momentFeed，用旧的链接解析方式
        post_links = soup.find_all('a', href=re.compile(r'/circle/\d+/detail/'))
        seen_ids = set()
        for link in post_links:
            href = link.get('href', '')
            match = re.search(r'/circle/(\d+)/detail/', href)
            if match:
                post_id = match.group(1)
                if post_id in seen_ids:
                    continue
                seen_ids.add(post_id)
                
                parent = link.find_parent(['div', 'article'])
                content = ""
                if parent:
                    text_parts = []
                    for p in parent.find_all(['p', 'div']):
                        text = p.get_text(strip=True)
                        if text and len(text) < 200:
                            text_parts.append(text)
                    content = " ".join(text_parts[:3])
                
                posts.append({
                    "id": post_id,
                    "title": content[:80] if content else f"帖子 {post_id}",
                    "url": f"{self.base_url}/circle/{post_id}/detail/",
                })
        
        return posts

    def get_post_details(self, post_id: str) -> Dict:
        """获取帖子详情"""
        try:
            resp = self.session.get(f"{self.base_url}/circle/{post_id}/detail/")
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            content = ""
            content_div = soup.find('div', class_=re.compile('prose|content|post|main'))
            if content_div:
                content = content_div.get_text(strip=True)
            else:
                paragraphs = soup.find_all('p')
                content_parts = []
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 5 and '前' not in text and '回复' not in text and '评论' not in text:
                        content_parts.append(text)
                content = ' '.join(content_parts[:5])
            
            images = []
            img_elements = soup.find_all('img')
            for img in img_elements:
                src = img.get('src', '')
                if src and '/media/moments/' in src:
                    if src.startswith('/'):
                        src = self.base_url + src
                    images.append(src)
            
            author = ""
            author_elem = soup.find('a', href=re.compile('/accounts/profile/'))
            if author_elem:
                author = author_elem.get_text(strip=True)
            
            return {
                "content": content[:500] if content else "",
                "images": images,
                "author": author,
            }
        except Exception as e:
            print(f"获取帖子详情失败: {e}")
            return {"content": "", "images": [], "author": ""}

    def comment(self, post_id: str, content: str) -> Dict:
        """评论指定帖子"""
        url = f"{self.base_url}/circle/{post_id}/comment/"
        csrf_token = self.session.cookies.get("csrftoken", "")
        
        try:
            resp = self.session.post(
                url,
                data={"content": content},
                headers={
                    "Referer": f"{self.base_url}/circle/{post_id}/detail/",
                    "X-CSRFToken": csrf_token,
                    "X-Requested-With": "XMLHttpRequest"
                }
            )
            
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    if data.get("id"):
                        return {"success": True, "message": "评论成功", "data": data}
                except:
                    pass
                    
                if "成功" in resp.text or "id" in resp.text:
                    return {"success": True, "message": "评论成功", "data": resp.text}
            
            return {"success": False, "message": f"评论失败: HTTP {resp.status_code}"}
            
        except Exception as e:
            return {"success": False, "message": str(e)}

    def like(self, post_id: str) -> Dict:
        """点赞指定帖子"""
        url = f"{self.base_url}/circle/{post_id}/like/"
        csrf_token = self.session.cookies.get("csrftoken", "")
        
        try:
            resp = self.session.post(
                url,
                headers={
                    "Referer": f"{self.base_url}/circle/{post_id}/detail/",
                    "X-CSRFToken": csrf_token,
                    "X-Requested-With": "XMLHttpRequest"
                }
            )
            
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    return {"success": True, "message": "点赞成功", "data": data}
                except:
                    pass
                if "liked" in resp.text.lower() or "success" in resp.text.lower():
                    return {"success": True, "message": "点赞成功"}
            
            return {"success": False, "message": f"点赞失败: HTTP {resp.status_code}"}
            
        except Exception as e:
            return {"success": False, "message": str(e)}

    def get_posts_for_commenting(
        self,
        pages: int = 2,
        sorts: list = None,
        fetch_details: bool = True,
    ) -> List[Dict]:
        """
        获取需要评论的帖子列表（专供 MCP 图文理解流程使用）
        
        流程：
        1. 调用本方法获取帖子列表（含图片URL）
        2. 对每个帖子的图片调用 MiniMax MCP understand_image 工具
        3. 根据理解结果生成评论
        4. 调用 comment(post_id, 评论内容) 提交
        
        Args:
            pages: 扫描页数
            sorts: 排序方式列表，默认为 ["new", "hot", "following"]
            fetch_details: 是否获取每个帖子的详情（默认True）。
                          当为 False 时，直接使用 get_circle_posts 返回的基本信息，
                          跳过对每个帖子的详情请求，速度更快，但 content 可能只包含摘要。
                          **MCP 图文理解场景建议用 True**，因为图片URL在详情中更完整。
                          **快速扫描场景用 False**，只检查 post_id 和图片URL。
        
        Returns:
            List[Dict]: 帖子列表（去重），每项包含 post_id, content, images, author, url
        """
        if sorts is None:
            # 评论优先扫描最新帖子 new > hot > following，确保评论新鲜内容
            sorts = ["new", "hot", "following"]
        
        all_posts = []
        seen_ids = set()
        
        for sort in sorts:
            before = None
            for page in range(1, pages + 1):
                posts = self.get_circle_posts(before=before, sort=sort)
                if not posts:
                    break

                # 记录最后一条帖子 id，作为下一页的 before 参数
                before = posts[-1]["id"]

                for post in posts:
                    if post["id"] in seen_ids:
                        continue

                    if fetch_details:
                        # 完整模式：获取每个帖子的详情（包括完整图片列表）
                        details = self.get_post_details(post["id"])
                        images = details.get("images", [])
                        content = details.get("content", "")
                        author = details.get("author", "")
                    else:
                        # 快速模式：直接使用 get_circle_posts 的基本信息
                        images = post.get("images", [])
                        content = post.get("content", "")
                        author = post.get("author", "") or ""
                        details = None

                    # 过滤广告推广帖（平台追加推广文字，提取主内容判断）
                    main_content = content.split("好友通过你的链接注册")[0].strip()
                    if len(main_content) < 5:
                        continue

                    if images:
                        seen_ids.add(post["id"])
                        all_posts.append({
                            "post_id": post["id"],
                            "content": main_content,
                            "images": images,
                            "author": author,
                            "url": f"{self.base_url}/circle/{post['id']}/detail/",
                        })
        
        return all_posts

    # ========== 辅助功能 ==========

    def get_user_info(self) -> Dict:
        """获取当前登录用户信息"""
        try:
            resp = self.session.get(f"{self.base_url}/circle/")
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            user_dropdown = soup.find('div', {'id': 'userDropdown'})
            if user_dropdown:
                username = user_dropdown.get_text(strip=True)
                return {"username": username, "logged_in": True}
            
            login_link = soup.find('a', href='/accounts/login/')
            if login_link:
                return {"logged_in": False}
                
            return {"logged_in": True}
        except Exception as e:
            return {"logged_in": False, "error": str(e)}


