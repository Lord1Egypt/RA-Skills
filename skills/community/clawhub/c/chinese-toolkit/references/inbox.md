# 收件箱和消息管理
## 技能消息处理、通知管理和通信系统

## 🎯 消息管理系统架构

### 1. 消息处理流程
```
端到端消息处理:
• 接收: 从多个渠道接收消息
• 分类: 自动分类消息类型
• 路由: 根据规则路由到处理者
• 处理: 人工或自动处理消息
• 归档: 存储处理结果和历史
• 分析: 分析消息数据和趋势
```

### 2. 消息类型分类
```
消息分类体系:
📧 用户反馈
├── 功能建议
├── Bug报告
├── 使用问题
└── 改进意见

🔔 系统通知
├── 状态更新
├── 维护通知
├── 安全警报
└── 版本发布

📊 数据报告
├── 使用统计
├── 性能报告
├── 错误报告
└── 趋势分析

🤝 合作请求
├── 技术合作
├── 商业合作
├── 社区合作
└── 媒体采访

📝 文档请求
├── 文档更新
├── 翻译请求
├── 示例请求
└── 教程请求
```

## 📨 收件箱系统实现

### 1. 统一收件箱系统
#### 核心收件箱类：
```python
# inbox_system.py
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json
import email
import re

class MessageType(Enum):
    EMAIL = "email"
    WEB_FORM = "web_form"
    API = "api"
    SYSTEM = "system"
    CHAT = "chat"

class MessageStatus(Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"
    DELETED = "deleted"
    SPAM = "spam"

class Priority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4

class InboxSystem:
    def __init__(self, db_path: str = "inbox.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 消息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT UNIQUE NOT NULL,
                message_type TEXT NOT NULL,
                sender TEXT NOT NULL,
                recipient TEXT NOT NULL,
                subject TEXT,
                body TEXT NOT NULL,
                html_body TEXT,
                priority INTEGER DEFAULT 2,
                status TEXT DEFAULT 'unread',
                category TEXT,
                tags TEXT,
                metadata TEXT,
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                read_at TIMESTAMP,
                processed_at TIMESTAMP,
                assigned_to TEXT,
                thread_id TEXT,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES messages (id)
            )
        ''')
        
        # 附件表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                content_type TEXT,
                file_size INTEGER,
                file_path TEXT,
                storage_type TEXT DEFAULT 'local',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (message_id) REFERENCES messages (id)
            )
        ''')
        
        # 标签表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 消息-标签关联表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_tags (
                message_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (message_id, tag_id),
                FOREIGN KEY (message_id) REFERENCES messages (id),
                FOREIGN KEY (tag_id) REFERENCES tags (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def receive_message(self, message_type: MessageType, sender: str, 
                       recipient: str, body: str, subject: str = None,
                       html_body: str = None, metadata: Dict = None,
                       attachments: List[Dict] = None) -> int:
        """接收新消息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 生成唯一消息ID
        message_id = f"msg_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(sender)}"
        
        # 解析和分类消息
        category = self._classify_message(subject, body)
        priority = self._determine_priority(sender, subject, body)
        tags = self._extract_tags(subject, body)
        
        metadata_json = json.dumps(metadata) if metadata else '{}'
        
        # 插入消息
        cursor.execute('''
            INSERT INTO messages 
            (message_id, message_type, sender, recipient, subject, body, 
             html_body, priority, category, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (message_id, message_type.value, sender, recipient, subject, body,
              html_body, priority.value, category, metadata_json))
        
        message_db_id = cursor.lastrowid
        
        # 处理附件
        if attachments:
            for attachment in attachments:
                cursor.execute('''
                    INSERT INTO attachments 
                    (message_id, filename, content_type, file_size, file_path)
                    VALUES (?, ?, ?, ?, ?)
                ''', (message_db_id, attachment.get('filename'),
                      attachment.get('content_type'), attachment.get('file_size'),
                      attachment.get('file_path')))
        
        # 添加标签
        for tag_name in tags:
            tag_id = self._get_or_create_tag(tag_name, cursor)
            cursor.execute('''
                INSERT OR IGNORE INTO message_tags (message_id, tag_id)
                VALUES (?, ?)
            ''', (message_db_id, tag_id))
        
        conn.commit()
        conn.close()
        
        # 触发通知
        self._notify_new_message(message_db_id)
        
        return message_db_id
    
    def _classify_message(self, subject: str, body: str) -> str:
        """分类消息"""
        text = (subject or '') + ' ' + (body or '')
        text_lower = text.lower()
        
        # 基于关键词分类
        categories = {
            'bug': ['bug', 'error', 'crash', '失败', '错误'],
            'feature': ['feature', '功能', '建议', '希望'],
            'question': ['question', '问题', '如何', '怎么'],
            'support': ['help', '支持', '求助', '救命'],
            'feedback': ['feedback', '反馈', '意见'],
            'spam': ['buy', 'sell', '赚钱', '促销']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def _determine_priority(self, sender: str, subject: str, body: str) -> Priority:
        """确定消息优先级"""
        text = (subject or '') + ' ' + (body or '')
        text_lower = text.lower()
        
        # 紧急关键词
        urgent_keywords = ['urgent', '紧急', 'crash', '宕机', 'broken', '坏了']
        high_keywords = ['important', '重要', 'help', '求助', 'error', '错误']
        
        if any(keyword in text_lower for keyword in urgent_keywords):
            return Priority.URGENT
        elif any(keyword in text_lower for keyword in high_keywords):
            return Priority.HIGH
        elif 'low' in text_lower or '低' in text_lower:
            return Priority.LOW
        
        return Priority.NORMAL
    
    def _extract_tags(self, subject: str, body: str) -> List[str]:
        """提取标签"""
        text = (subject or '') + ' ' + (body or '')
        tags = []
        
        # 提取#标签
        hashtags = re.findall(r'#(\w+)', text)
        tags.extend(hashtags)
        
        # 提取关键词作为标签
        keywords = ['api', 'ui', 'performance', 'security', 'documentation',
                   '安装', '配置', '使用', '问题']
        
        for keyword in keywords:
            if keyword in text.lower():
                tags.append(keyword)
        
        return list(set(tags))
    
    def _get_or_create_tag(self, tag_name: str, cursor) -> int:
        """获取或创建标签"""
        cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            cursor.execute('''
                INSERT INTO tags (name, color)
                VALUES (?, ?)
            ''', (tag_name, self._generate_tag_color(tag_name)))
            return cursor.lastrowid
    
    def _generate_tag_color(self, tag_name: str) -> str:
        """生成标签颜色"""
        # 简单哈希生成颜色
        import hashlib
        hash_obj = hashlib.md5(tag_name.encode())
        hash_hex = hash_obj.hexdigest()[:6]
        return f'#{hash_hex}'
    
    def _notify_new_message(self, message_id: int):
        """通知新消息"""
        # 这里可以集成邮件、Slack、Webhook等通知方式
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT subject, sender, priority FROM messages WHERE id = ?
        ''', (message_id,))
        
        message = cursor.fetchone()
        conn.close()
        
        if message:
            subject, sender, priority = message
            print(f"📨 新消息: {subject} (来自: {sender}, 优先级: {priority})")
    
    def get_inbox(self, status: str = None, category: str = None, 
                 tag: str = None, priority: int = None, 
                 limit: int = 50, offset: int = 0) -> List[Dict]:
        """获取收件箱消息"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        conditions = ["status != 'deleted'"]
        params = []
        
        if status:
            conditions.append("status = ?")
            params.append(status)
        
        if category:
            conditions.append("category = ?")
            params.append(category)
        
        if priority:
            conditions.append("priority = ?")
            params.append(priority)
        
        if tag:
            conditions.append('''
                EXISTS (
                    SELECT 1 FROM message_tags mt
                    JOIN tags t ON mt.tag_id = t.id
                    WHERE mt.message_id = messages.id AND t.name = ?
                )
            ''')
            params.append(tag)
        
        where_clause = " AND ".join(conditions)
        params.extend([limit, offset])
        
        query = f'''
            SELECT m.*, 
                   GROUP_CONCAT(t.name) as tag_names,
                   COUNT(a.id) as attachment_count
            FROM messages m
            LEFT JOIN message_tags mt ON m.id = mt.message_id
            LEFT JOIN tags t ON mt.tag_id = t.id
            LEFT JOIN attachments a ON m.id = a.message_id
            WHERE {where_clause}
            GROUP BY m.id
            ORDER BY 
                CASE priority
                    WHEN 4 THEN 1  -- URGENT
                    WHEN 3 THEN 2  -- HIGH
                    WHEN 2 THEN 3  -- NORMAL
                    ELSE 4         -- LOW
                END,
                received_at DESC
            LIMIT ? OFFSET ?
        '''
        
        cursor.execute(query, params)
        messages = cursor.fetchall()
        
        result = []
        for message in messages:
            message_dict = dict(message)
            
            # 解析标签
            if message_dict['tag_names']:
                message_dict['tags'] = message_dict['tag_names'].split(',')
            else:
                message_dict['tags'] = []
            
            # 解析元数据
            if message_dict['metadata']:
                message_dict['metadata'] = json.loads(message_dict['metadata'])
            else:
                message_dict['metadata'] = {}
            
            result.append(message_dict)
        
        conn.close()
        return result
    
    def mark_as_read(self, message_id: int):
        """标记消息为已读"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE messages 
            SET status = 'read', read_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (message_id,))
        
        conn.commit()
        conn.close()
    
    def archive_message(self, message_id: int):
        """归档消息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE messages 
            SET status = 'archived', processed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (message_id,))
        
        conn.commit()
        conn.close()
    
    def assign_message(self, message_id: int, assignee: str):
        """分配消息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE messages 
            SET assigned_to = ?
            WHERE id = ?
        ''', (assignee, message_id))
        
        conn.commit()
        conn.close()
    
    def add_reply(self, message_id: int, sender: str, body: str, 
                 is_internal: bool = False):
        """添加回复"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取原始消息
        cursor.execute('SELECT message_id, subject FROM messages WHERE id = ?', 
                      (message_id,))
        original = cursor.fetchone()
        
        if original:
            original_message_id, original_subject = original
            
            # 创建回复消息
            reply_subject = f"Re: {original_subject}" if original_subject else None
            reply_message_id = f"reply_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            cursor.execute('''
                INSERT INTO messages 
                (message_id, message_type, sender, recipient, subject, body, 
                 priority, category, parent_id, thread_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (reply_message_id, 'system' if is_internal else 'email',
                  sender, 'system', reply_subject, body, 2, 'reply',
                  message_id, original_message_id))
            
            conn.commit()
        
        conn.close()
```

### 2. 邮件集成系统
#### 邮件接收和处理：
```python
# email_integration.py
import imaplib
import email
from email.header import decode_header
from typing import List, Dict
import re

class EmailIntegration:
    def __init__(self, imap_server: str, email_address: str, password: str):
        self.imap_server = imap_server
        self.email_address = email_address
        self.password = password
        self.mail = None
    
    def connect(self):
        """连接到邮件服务器"""
        self.mail = imaplib.IMAP4_SSL(self.imap_server)
        self.mail.login(self.email_address, self.password)
        self.mail.select('inbox')
    
    def disconnect(self):
        """断开连接"""
        if self.mail:
            self.mail.logout()
            self.mail = None
    
    def fetch_unread_emails(self) -> List[Dict]:
        """获取未读邮件"""
        if not self.mail:
            self.connect()
        
        # 搜索未读邮件
        status, messages = self.mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        
        emails = []
        for email_id in email_ids:
            email_data = self._fetch_email(email_id)
            if email_data:
                emails.append(email_data)
        
        return emails
    
    def _fetch_email(self, email_id: bytes) -> Dict:
        """获取单个邮件"""
        status, msg_data = self.mail.fetch(email_id, '(RFC822)')
        
        if status != 'OK':
            return None
        
        # 解析邮件
        msg = email.message_from_bytes(msg_data[0][1])
        
        # 解码主题
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else 'utf-8')
        
        # 获取发件人
        from_ = msg.get("From")
        
        # 获取邮件正文
        body = self._extract_body(msg)
        
        # 获取附件
        attachments = self._extract_attachments(msg)
        
        return {
            'id': email_id.decode(),
            'subject': subject,
            'from': from_,
            'body': body,
            'attachments': attachments,
            'date': msg.get("Date"),
            'message_id': msg.get("Message-ID")
        }
    
    def _extract_body(self, msg) -> str:
        """提取邮件正文"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # 跳过附件
                if "attachment" in content_disposition:
                    continue
                
                # 获取文本内容
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
                elif content_type == "text/html":
                    # 如果没有纯文本，使用HTML
                    if not body:
                        body = part.get_payload(decode=True).