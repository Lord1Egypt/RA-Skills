import os
import sqlite3
import email
from email import policy
from email.utils import parsedate_to_datetime
import hashlib
from datetime import datetime
from tqdm import tqdm

def get_file_hash(file_path):
    """計算檔案的 MD5 hash 以用於去重"""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def extract_eml_info(file_path):
    """解析 EML 檔案並提取關鍵資訊"""
    try:
        with open(file_path, 'rb') as f:
            msg = email.message_from_binary_file(f, policy=policy.default)
        
        subject = msg.get('subject', '(無主旨)')
        sender = msg.get('from', '(未知寄件者)')
        recipient = msg.get('to', '(未知收件者)')
        
        # 處理日期
        date_str = msg.get('date')
        if date_str:
            try:
                dt = parsedate_to_datetime(date_str)
                sent_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                sent_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            sent_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
        # 提取內文 (優先取純文字)
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_content()
                    break
            if not body: # 如果沒有純文字，嘗試取 HTML 並簡單處理
                for part in msg.walk():
                    if part.get_content_type() == 'text/html':
                        body = part.get_content()
                        break
        else:
            body = msg.get_content()
            
        return {
            'subject': subject,
            'sender': sender,
            'recipient': recipient,
            'sent_time': sent_time,
            'body': body,
            'file_path': file_path,
            'file_hash': get_file_hash(file_path)
        }
    except Exception as e:
        print(f"解析錯誤 {file_path}: {e}")
        return None

def init_db(db_path):
    """初始化 SQLite 資料庫"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_hash TEXT UNIQUE,
            subject TEXT,
            sender TEXT,
            recipient TEXT,
            sent_time TEXT,
            body TEXT,
            file_path TEXT,
            indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def index_directory(directory, db_path):
    """掃描目錄並索引 EML 檔案"""
    conn = init_db(db_path)
    cursor = conn.cursor()
    
    eml_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.eml'):
                eml_files.append(os.path.join(root, file))
    
    print(f"🔍 找到 {len(eml_files)} 個 EML 檔案，開始索引...")
    
    new_count = 0
    skip_count = 0
    
    for i, file_path in enumerate(tqdm(eml_files)):
        file_hash = get_file_hash(file_path)
        
        # 檢查是否已存在
        cursor.execute("SELECT id FROM emails WHERE file_hash = ?", (file_hash,))
        if cursor.fetchone():
            skip_count += 1
            continue
            
        info = extract_eml_info(file_path)
        if info:
            try:
                cursor.execute('''
                    INSERT INTO emails (file_hash, subject, sender, recipient, sent_time, body, file_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (info['file_hash'], info['subject'], info['sender'], info['recipient'], info['sent_time'], info['body'], info['file_path']))
                new_count += 1
            except sqlite3.IntegrityError:
                skip_count += 1
        
        # 每 100 筆提交一次
        if (i + 1) % 100 == 0:
            conn.commit()
                
    conn.commit()
    conn.close()
    print(f"✅ 索引完成！新增: {new_count}, 跳過(重複): {skip_count}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法: python indexer.py <EML目錄> <資料庫路徑>")
    else:
        index_directory(sys.argv[1], sys.argv[2])
