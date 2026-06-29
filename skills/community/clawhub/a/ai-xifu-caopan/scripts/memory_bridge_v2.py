#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小媳妇记忆续接系统 v2.0
Memory Bridge System v2.0

完整流程:
1. 白天:实时备份聊天数据 + 方案文件 到本地库
2. 上传到云端服务器(预留)
3. 晚上00:00:自动拉取昨日数据
4. 醒来:自动执行昨日数据,恢复记忆

作者:大叔的药方
版本:v2.0
"""

import os
import json
import shutil
import glob
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 路径配置
WORKSPACE = "/home/sandbox/.openclaw/workspace"
MEMORY_DIR = f"{WORKSPACE}/memory"
CHAT_BACKUP_DIR = f"{MEMORY_DIR}/chat_backup"
SESSION_ARCHIVE = f"{MEMORY_DIR}/session_archive"
SKILL_PATH = f"{WORKSPACE}/skills/ai-xifu-caopan"

class MemoryBridgeV2:
    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.now = datetime.now().strftime('%H:%M:%S')

    def extract_today_memory(self):
        """从今天会话中提取聊天记录，写入日常记忆文件"""
        print()
        print("📝 提取今日聊天记录写入记忆...")

        session_patterns = [
            os.path.expanduser("~/.openclaw/agents/main/sessions/*.jsonl"),
        ]

        # 收集今天的对话 — 按每条消息的实际 CST 时间戳过滤，不再依赖文件 mtime
        # 🐛 修复前：用 getmtime() 判断文件是否今天→可能把昨天文件混入
        # ✅ 修复后：读所有 .jsonl 会话文件，但只提取 CST 时间属于今天的消息
        #    会话文件时间戳为 UTC → 转 CST（UTC+8）再比较
        today_chats = []  # [(cst_time, 角色, 内容)]
        today_cst = self.today  # 已经初始化为 CST 日期
        from datetime import timezone, timedelta
        cst_offset = timezone(timedelta(hours=8))

        for pattern in session_patterns:
            for filepath in glob.glob(pattern):
                # 跳过 trajectory（轨迹文件存工具调用，非对话）
                if ".trajectory" in filepath or ".reset" in filepath:
                    continue
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                obj = json.loads(line)
                                if obj.get('type') != 'message':
                                    continue
                                # ✅ 关键修复：用消息的实际时间戳判断是否属于今天
                                ts_utc_str = obj.get('timestamp', '')
                                if not ts_utc_str or len(ts_utc_str) < 19:
                                    continue
                                # 解析UTC时间 → 转CST
                                ts_utc_dt = datetime.fromisoformat(ts_utc_str.replace('Z', '+00:00'))
                                ts_cst_dt = ts_utc_dt.astimezone(cst_offset)
                                msg_date_cst = ts_cst_dt.strftime('%Y-%m-%d')
                                if msg_date_cst != today_cst:
                                    continue

                                msg = obj.get('message', {})
                                role = msg.get('role', '')
                                if role not in ('user', 'assistant'):
                                    continue
                                # 提取对话内容
                                content_parts = msg.get('content', [])
                                if isinstance(content_parts, list):
                                    text = ' '.join([
                                        c.get('text', '') for c in content_parts
                                        if isinstance(c, dict) and c.get('type') == 'text'
                                    ])
                                else:
                                    text = str(content_parts)[:200]

                                if not text.strip():
                                    continue

                                time_str = ts_cst_dt.strftime('%H:%M:%S')
                                today_chats.append((time_str, role, text.strip()))
                            except (json.JSONDecodeError, Exception):
                                pass
                except Exception:
                    pass

        # 去重（同一时间同一内容只保留一次）
        seen = set()
        unique_chats = []
        for ts, role, text in today_chats:
            key = f"{ts}_{role}_{text[:50]}"
            if key not in seen:
                seen.add(key)
                unique_chats.append((ts, role, text))

        unique_chats.sort()  # 按时间排序

        if not unique_chats:
            print(f"  i️ 今日无有效对话记录")
            return False

        # 写入日常记忆文件
        daily_file = f"{MEMORY_DIR}/{self.today}.md"

        # 构建内容
        lines = []
        lines.append(f"# {self.today} 日常对话日志\n")
        lines.append(f"_自动生成于 {self.now}_")
        lines.append("")

        # 统计
        user_msgs = sum(1 for _, r, _ in unique_chats if r == 'user')
        assistant_msgs = sum(1 for _, r, _ in unique_chats if r == 'assistant')
        lines.append(f"**今日对话统计:** 大叔说了 {user_msgs} 条,小媳妇回了 {assistant_msgs} 条")
        lines.append("")

        # 提取时间分段
        lines.append("---")
        lines.append("## 对话记录")
        lines.append("")

        current_hour = -1
        for ts, role, text in unique_chats:
            if not ts:
                ts = "--:--:--"
            hour = int(ts[:2]) if len(ts) >= 2 else -1
            if hour != current_hour and hour >= 0:
                current_hour = hour
                lines.append(f"### {hour:02d}:00 - {hour:02d}:59")
                lines.append("")

            prefix = "🧑 **大叔**" if role == 'user' else "🦊 **小媳妇**"
            lines.append(f"- **{ts}** {prefix}: {text}")

        lines.append("")
        lines.append("---")
        lines.append(f"_记录结束 - 共 {len(unique_chats)} 条消息_")
        lines.append("")

        # 读取已有内容(如果文件已有非自动生成内容,保留)
        existing_content = ""
        if os.path.exists(daily_file):
            with open(daily_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            # 如果已有手动添加的内容,追加到自动内容后面
            if existing_content.strip() and "日常对话日志" not in existing_content:
                lines.append("")
                lines.append("## 📝 手动备注\n")
                lines.append(existing_content)

        with open(daily_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"  ✅ 写入 {len(unique_chats)} 条对话到 {daily_file}")

        # 更新关键词索引
        self._update_keyword_index(unique_chats)

        return True

    def _update_keyword_index(self, chats):
        """更新关键词索引,方便快速检索"""
        index_file = f"{MEMORY_DIR}/keyword_index.json"

        # 提取关键词
        import re
        keywords = set()
        important_prefixes = ['国信', 'Tushare', '华为', '云盘', '备份', '模板', '方案',
                             '股票', '期货', '基金', '大盘', '数据', '接口', '授权',
                             '分析', '预判', '模型', '持仓', '交易', '夜盘',
                             '大叔', '小媳妇', '记忆', '设置', '配置', '安装']

        for _, _, text in chats:
            for kw in important_prefixes:
                if kw in text:
                    keywords.add(kw)

        # 加载已有索引
        index = {}
        if os.path.exists(index_file):
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    index = json.load(f)
            except:
                pass

        # 更新索引
        for kw in keywords:
            if kw not in index:
                index[kw] = []
            entry = {"date": self.today, "time": self.now}
            if entry not in index[kw]:
                index[kw].append(entry)

        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

        print(f"  🔑 关键词索引已更新: {len(keywords)} 个")

    def backup_all_today_data(self):
        """备份今天所有数据"""
        print("=" * 60)
        print("💾 备份今日全部数据")
        print("=" * 60)
        print(f"日期: {self.today} {self.now}")
        print()

        # 创建今日备份目录
        today_backup_dir = f"{CHAT_BACKUP_DIR}/{self.today}"
        os.makedirs(today_backup_dir, exist_ok=True)

        backed_files = []

        # 1. 备份OpenClaw会话文件(真正的聊天记录)
        print("📂 备份聊天记录...")
        session_patterns = [
            os.path.expanduser("~/.openclaw/agents/main/sessions/*.jsonl"),
            os.path.expanduser("~/.openclaw/agents/main/sessions/*.jsonl.gz"),
            os.path.expanduser("~/.openclaw/agents/main/sessions/*.json"),
        ]

        from datetime import timezone
        cst_offset = timezone(timedelta(hours=8))
        today_cst = self.today
        for pattern in session_patterns:
            for filepath in glob.glob(pattern):
                try:
                    filename = os.path.basename(filepath)
                    # 🐛 修复前:用 mtime 过滤 → 会把昨天被触碰的文件算成今天
                    # ✅ 修复后:扫描会话内是否有今天的消息(按 CST 时间) → 有才备份
                    has_today_msg = False
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f_check:
                        for _ in range(50):  # 最多读50行就够了
                            line = f_check.readline()
                            if not line:
                                break
                            try:
                                obj = json.loads(line.strip())
                                if obj.get('type') == 'message':
                                    ts_str = obj.get('timestamp', '')
                                    if len(ts_str) >= 19:
                                        ts_dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                                        ts_cst = ts_dt.astimezone(cst_offset).strftime('%Y-%m-%d')
                                        if ts_cst == today_cst:
                                            has_today_msg = True
                                            break
                            except:
                                pass
                    if has_today_msg:
                        dst = f"{today_backup_dir}/session_{filename}"
                        shutil.copy2(filepath, dst)
                        backed_files.append(f"session_{filename}")
                        print(f"  ✅ 会话: {filename}")
                except Exception as e:
                    print(f"  ⚠️ 跳过: {filename} ({e})")

        # 2. 备份记忆文件
        print()
        print("🧠 备份记忆文件...")
        memory_files = [
            (f"{MEMORY_DIR}/{self.today}.md", f"memory_today.md"),
            (f"{WORKSPACE}/MEMORY.md", "MEMORY.md"),
            (f"{WORKSPACE}/AGENTS.md", "AGENTS.md"),
            (f"{WORKSPACE}/USER.md", "USER.md"),
            (f"{WORKSPACE}/SOUL.md", "SOUL.md"),
        ]

        for src, dst_name in memory_files:
            if os.path.exists(src):
                dst = f"{today_backup_dir}/{dst_name}"
                shutil.copy2(src, dst)
                backed_files.append(dst_name)
                print(f"  ✅ {dst_name}")

        # 3. 备份媳妇智投Pro方案文件
        print()
        print("📊 备份媳妇智投Pro方案...")
        plan_patterns = [
            f"{SKILL_PATH}/templates/*.md",
            f"{SKILL_PATH}/*.md",
            f"{SKILL_PATH}/scripts/*.py",
        ]

        for pattern in plan_patterns:
            for filepath in glob.glob(pattern):
                try:
                    filename = os.path.basename(filepath)
                    dst = f"{today_backup_dir}/skill_{filename}"
                    if not os.path.exists(dst):
                        shutil.copy2(filepath, dst)
                        backed_files.append(f"skill_{filename}")
                        print(f"  ✅ 方案: {filename}")
                except Exception as e:
                    pass

        # 4. 备份生成的Word文档
        print()
        print("📄 备份生成的方案文档...")
        doc_patterns = [
            "/tmp/*.docx",
            f"{WORKSPACE}/*.docx",
        ]

        for pattern in doc_patterns:
            for filepath in glob.glob(pattern):
                try:
                    filename = os.path.basename(filepath)
                    # 🐛 修复：getmtime 跨日会误判（文件被触碰后mtime变成当天）
                    # ✅ 改用 getctime（元数据变动时间），生成文件不会变，ctime更可靠
                    ctime = datetime.fromtimestamp(os.path.getctime(filepath))
                    if ctime.strftime('%Y-%m-%d') == self.today:
                        dst = f"{today_backup_dir}/doc_{filename}"
                        shutil.copy2(filepath, dst)
                        backed_files.append(f"doc_{filename}")
                        print(f"  ✅ 文档: {filename}")
                except Exception as e:
                    pass

        # 5. 生成完整备份清单
        print()
        manifest = {
            "version": "2.0",
            "date": self.today,
            "backup_time": datetime.now().isoformat(),
            "files_count": len(backed_files),
            "files": backed_files,
            "categories": {
                "sessions": [f for f in backed_files if f.startswith("session_")],
                "memory": [f for f in backed_files if f in ["MEMORY.md", "AGENTS.md", "USER.md", "SOUL.md", "memory_today.md"]],
                "skills": [f for f in backed_files if f.startswith("skill_")],
                "documents": [f for f in backed_files if f.startswith("doc_")]
            }
        }

        manifest_path = f"{today_backup_dir}/manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        # 4. 自动提取持仓信息并写入每日记忆
        print()
        print("💼 自动提取持仓信息...")
        try:
            import subprocess
            extractor = f"{WORKSPACE}/memory/scripts/extract_positions.py"
            if os.path.exists(extractor):
                result = subprocess.run(
                    ["python3", extractor, "--date", self.today],
                    capture_output=True, text=True, timeout=30
                )
                output = result.stdout
                if output and len(output.strip()) > 10:
                    for line in output.strip().split(chr(10)):
                        print(f"  {line}")
                if result.stderr:
                    print(f"  ⚠️ 提取器stderr: {result.stderr[:200]}")
                print(f"  ✅ 持仓提取完成")
            else:
                print(f"  ⚠️ 提取器不存在, 跳过")
        except Exception as e:
            print(f"  ⚠️ 持仓提取失败: {e}")

        print()
        print("=" * 60)
        print(f"✅ 备份完成: {len(backed_files)} 个文件")
        print(f"📁 位置: {today_backup_dir}")
        print("=" * 60)

        return manifest

    def upload_to_huawei_drive(self):
        """上传今日备份到华为云盘"""
        print()
        print("📤 上传到华为云盘...")

        today_backup_dir = f"{CHAT_BACKUP_DIR}/{self.today}"
        if not os.path.exists(today_backup_dir):
            print(f"  ❌ 今日备份目录不存在: {today_backup_dir}")
            return False

        # 打包备份目录
        import tarfile
        archive_name = f"memory_backup_{self.today}.tar.gz"
        archive_path = f"/tmp/{archive_name}"

        try:
            with tarfile.open(archive_path, "w:gz") as tar:
                tar.add(today_backup_dir, arcname=self.today)
            archive_size = os.path.getsize(archive_path)
            print(f"  📦 打包完成: {archive_name} ({archive_size/1024:.1f} KB)")
        except Exception as e:
            print(f"  ❌ 打包失败: {e}")
            return False

        # 检查云盘可用空间
        hdrive_script = os.path.expanduser(
            "~/.openclaw/workspace/skills/huawei-drive/scripts/huawei_drive.py"
        )
        if not os.path.exists(hdrive_script):
            print(f"  ❌ 云盘脚本不存在: {hdrive_script}")
            os.remove(archive_path)
            return False

        import subprocess

        # 查询可用空间
        result = subprocess.run(
            ["python3", hdrive_script, "--command", "query", "--key", "available_space"],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout.strip()
        try:
            available = int(output)
            print(f"  💾 云盘可用空间: {available/1024/1024/1024:.1f} GB")
            if available < archive_size:
                print(f"  ❌ 云盘空间不足")
                os.remove(archive_path)
                return False
        except ValueError:
            print(f"  ⚠️ 无法获取云盘空间: {output[:100]}")

        # 上传到云盘(覆盖模式,保持最新备份)
        result = subprocess.run(
            ["python3", hdrive_script, "--command", "upload", "--mode", "overwrite", "--path", archive_path],
            capture_output=True, text=True, timeout=60
        )

        if "success" in result.stdout.lower():
            print(f"  ✅ 上传成功: 小艺Claw/{archive_name}")
        else:
            print(f"  ❌ 上传失败: {result.stdout[:200]}")
            if "TOKEN_EXPIRED" in result.stdout:
                print("  ⚠️ Token过期,需重新授权")
            print()
            print("=" * 60)
            print("🔴🔴🔴 紧急告警:云盘备份已连续失败!")
            print("=" * 60)
            print("⚠️ 原因:华为云盘Token已过期,自动上传被阻断")
            print("⚠️ 影响:云端无备份,一旦本地损毁数据将不可恢复")
            print("⚠️ 解决:请大叔重新启动小艺Claw完成华为云盘授权")
            print("=" * 60)
            print()
            os.remove(archive_path)
            return False

        # 清理本地临时归档
        os.remove(archive_path)
        print(f"  🧹 临时文件已清理")
        print(f"  ✅ 云盘备份完成")
        return True

    def pull_yesterday_and_restore(self):
        """拉取昨日数据并恢复(晚上00:00执行)"""
        print("=" * 60)
        print("📥 拉取昨日数据并恢复")
        print("=" * 60)
        print(f"执行时间: {self.now}")
        print(f"目标日期: {self.yesterday}")
        print()

        yesterday_backup = f"{CHAT_BACKUP_DIR}/{self.yesterday}"

        if not os.path.exists(yesterday_backup):
            print(f"❌ 昨日备份不存在: {yesterday_backup}")
            return False

        # 读取昨日清单
        manifest_path = f"{yesterday_backup}/manifest.json"
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            print(f"📋 昨日备份: {manifest['files_count']} 个文件")
            print(f"   备份时间: {manifest.get('backup_time', 'unknown')}")

        # 归档到session_archive
        archive_dir = f"{SESSION_ARCHIVE}/{self.yesterday}"
        if os.path.exists(archive_dir):
            shutil.rmtree(archive_dir)
        shutil.copytree(yesterday_backup, archive_dir)
        print(f"✅ 归档到: {archive_dir}")

        # 恢复关键文件
        print()
        print("🔄 恢复关键文件...")

        restore_map = {
            "MEMORY.md": f"{WORKSPACE}/MEMORY.md",
            "AGENTS.md": f"{WORKSPACE}/AGENTS.md",
            "memory_today.md": f"{MEMORY_DIR}/{self.yesterday}.md",
        }

        for src_name, dst_path in restore_map.items():
            src = f"{archive_dir}/{src_name}"
            if os.path.exists(src):
                shutil.copy2(src, dst_path)
                print(f"  ✅ 恢复: {src_name} -> {dst_path}")

        print()
        print("=" * 60)
        print("✅ 昨日数据已恢复!")
        print("=" * 60)

        return True

    def wake_and_load_memory(self):
        """醒来时加载记忆"""
        print("=" * 60)
        print("🧠 醒来加载记忆")
        print("=" * 60)
        print(f"时间: {self.now}")
        print()

        # 1. 检查昨日归档
        yesterday_archive = f"{SESSION_ARCHIVE}/{self.yesterday}"
        if os.path.exists(yesterday_archive):
            manifest_path = f"{yesterday_archive}/manifest.json"
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                print(f"✅ 发现昨日归档: {manifest['files_count']} 个文件")
                print(f"   日期: {manifest['date']}")
                print(f"   备份时间: {manifest.get('backup_time', 'unknown')}")

                # 显示分类统计
                categories = manifest.get('categories', {})
                for cat, files in categories.items():
                    if files:
                        print(f"   - {cat}: {len(files)} 个")
        else:
            print(f"⚠️ 昨日归档不存在: {self.yesterday}")

        # 2. 加载长期记忆
        print()
        print("📖 加载记忆文件...")
        memory_files = [
            ("长期记忆", f"{WORKSPACE}/MEMORY.md"),
            ("启动流程", f"{WORKSPACE}/AGENTS.md"),
            ("用户偏好", f"{WORKSPACE}/USER.md"),
            ("灵魂文件", f"{WORKSPACE}/SOUL.md"),
            ("今日记忆", f"{MEMORY_DIR}/{self.today}.md"),
            ("昨日记忆", f"{MEMORY_DIR}/{self.yesterday}.md"),
        ]

        for name, path in memory_files:
            if os.path.exists(path):
                size = os.path.getsize(path)
                print(f"  ✅ {name}: {size} 字节")
            else:
                print(f"  ⚠️ {name}: 不存在")

        # 3. 加载媳妇智投Pro模板
        print()
        print("📊 加载媳妇智投Pro模板...")
        template_path = f"{SKILL_PATH}/templates/FINAL_PLAN_TEMPLATE.md"
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if "v7.0 FINAL" in content:
                print(f"  ✅ 模板版本: v7.0 FINAL")
            else:
                print(f"  ⚠️ 模板版本可能不对")

        rules_path = f"{SKILL_PATH}/AUTO_ANALYSIS_RULES.md"
        if os.path.exists(rules_path):
            print(f"  ✅ 分析规则: 已加载")

        print()
        print("=" * 60)
        print("✅ 记忆加载完成,准备就绪!")
        print("=" * 60)

        return True

def main():
    import argparse
    parser = argparse.ArgumentParser(description='记忆续接系统 v2.0')
    parser.add_argument('--mode', type=str, default='backup',
                       choices=['backup', 'pull', 'wake', 'all', 'backup_cloud'],
                       help='运行模式: backup=备份, pull=拉取恢复, wake=醒来加载, all=完整流程, backup_cloud=备份+上传云盘')

    args = parser.parse_args()

    bridge = MemoryBridgeV2()

    if args.mode == 'backup':
        bridge.backup_all_today_data()
    elif args.mode == 'pull':
        bridge.pull_yesterday_and_restore()
    elif args.mode == 'wake':
        bridge.wake_and_load_memory()
    elif args.mode == 'backup_cloud':
        bridge.extract_today_memory()
        bridge.backup_all_today_data()
        bridge.upload_to_huawei_drive()
    else:  # all
        bridge.extract_today_memory()
        bridge.backup_all_today_data()
        bridge.upload_to_huawei_drive()
        bridge.wake_and_load_memory()

if __name__ == "__main__":
    main()
