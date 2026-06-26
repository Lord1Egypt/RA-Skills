# SVN 工作副本数据库查询指南

当无法连接 SVN 服务器时，可以直接查询本地工作副本数据库获取基本信息。

## 数据库位置

SVN 1.7+ 使用 SQLite 数据库存储工作副本信息：

```
项目目录/.svn/wc.db
```

## 数据库结构

### 主要表

| 表名 | 说明 |
|------|------|
| `NODES` | 工作副本节点信息（文件、目录） |
| `PRISTINE` | 文件内容缓存（基线版本） |
| `REPOSITORY` | 仓库信息（URL、UUID） |
| `LOCK` | 锁信息 |
| `WORK_QUEUE` | 工作队列 |

### NODES 表重要字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `wc_id` | INTEGER | 工作副本 ID（通常为 1） |
| `local_relpath` | TEXT | 相对于工作副本根目录的路径 |
| `op_depth` | INTEGER | 操作深度（0 = 基线版本） |
| `repos_id` | INTEGER | 仓库 ID |
| `repos_path` | TEXT | 仓库中的路径 |
| `revision` | INTEGER | 当前版本号 |
| `changed_revision` | INTEGER | 最后修改的版本号 |
| `changed_date` | INTEGER | 最后修改时间（微秒时间戳） |
| `changed_author` | TEXT | 最后修改者 |
| `kind` | TEXT | 类型（file/dir） |
| `presence` | TEXT | 存在状态（normal/absent等） |
| `checksum` | TEXT | 文件内容 SHA1 校验和 |

## 常用查询示例

### 1. 获取仓库信息

```python
import sqlite3

db_path = '/path/to/project/.svn/wc.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, root FROM REPOSITORY")
for repo_id, repo_url in cursor.fetchall():
    print(f"仓库 ID: {repo_id}")
    print(f"仓库 URL: {repo_url}")
```

### 2. 查询指定作者修改的所有文件

```python
import sqlite3
from datetime import datetime

db_path = '/path/to/project/.svn/wc.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

author_name = "liangyixiong"

cursor.execute("""
    SELECT 
        local_relpath,
        changed_revision,
        changed_date,
        kind
    FROM NODES
    WHERE wc_id = 1 
        AND op_depth = 0
        AND changed_author LIKE ?
    ORDER BY changed_date DESC
""", (f'%{author_name}%',))

for path, rev, date_ts, kind in cursor.fetchall():
    date = datetime.utcfromtimestamp(date_ts / 1000000)
    print(f"r{rev} | {date.strftime('%Y-%m-%d %H:%M')} | {kind} | {path}")
```

### 3. 查询修订版本统计

```python
cursor.execute("""
    SELECT 
        changed_revision,
        changed_author,
        MIN(changed_date) as date,
        COUNT(*) as file_count
    FROM NODES
    WHERE wc_id = 1 AND op_depth = 0
    GROUP BY changed_revision, changed_author
    ORDER BY changed_revision DESC
""")

print("修订版本统计:")
for rev, author, date_ts, count in cursor.fetchall():
    date = datetime.utcfromtimestamp(date_ts / 1000000)
    print(f"r{rev}: {author} 修改了 {count} 个文件 ({date.strftime('%Y-%m-%d')})")
```

### 4. 查询所有作者的修改统计

```python
cursor.execute("""
    SELECT 
        changed_author,
        COUNT(*) as file_count,
        COUNT(DISTINCT changed_revision) as rev_count
    FROM NODES
    WHERE wc_id = 1 AND op_depth = 0
    GROUP BY changed_author
    ORDER BY file_count DESC
""")

print("作者贡献统计:")
for author, file_count, rev_count in cursor.fetchall():
    print(f"{author}: {file_count} 个文件, {rev_count} 个提交")
```

### 5. 查询文件类型分布

```python
cursor.execute("""
    SELECT 
        CASE 
            WHEN local_relpath LIKE '%.c' THEN '.c'
            WHEN local_relpath LIKE '%.h' THEN '.h'
            WHEN local_relpath LIKE '%.cpp' THEN '.cpp'
            WHEN local_relpath LIKE '%.py' THEN '.py'
            WHEN local_relpath LIKE '%.js' THEN '.js'
            ELSE '其他'
        END as file_type,
        COUNT(*) as count
    FROM NODES
    WHERE wc_id = 1 AND op_depth = 0 AND kind = 'file'
    GROUP BY file_type
    ORDER BY count DESC
""")

print("文件类型分布:")
for file_type, count in cursor.fetchall():
    print(f"{file_type}: {count} 个文件")
```

### 6. 查询指定目录的修改历史

```python
directory = "libdrv"

cursor.execute("""
    SELECT 
        local_relpath,
        changed_revision,
        changed_author,
        changed_date
    FROM NODES
    WHERE wc_id = 1 
        AND op_depth = 0
        AND local_relpath LIKE ?
    ORDER BY changed_date DESC
""", (f'{directory}/%',))

print(f"{directory} 目录修改历史:")
for path, rev, author, date_ts in cursor.fetchall():
    date = datetime.utcfromtimestamp(date_ts / 1000000)
    print(f"r{rev} | {author} | {date.strftime('%Y-%m-%d %H:%M')} | {path}")
```

## 生成详细报告脚本

```python
#!/usr/bin/env python3
import sqlite3
from datetime import datetime
import sys

def generate_svn_report(db_path, author=None):
    """生成 SVN 本地数据库报告"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取仓库信息
    cursor.execute("SELECT root FROM REPOSITORY")
    repo_url = cursor.fetchone()[0]
    
    print("=" * 80)
    print(f"SVN 提交记录报告")
    print("=" * 80)
    print(f"仓库: {repo_url}")
    print(f"作者: {author or '所有'}")
    print(f"数据来源: 本地工作副本数据库")
    print(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 查询修改记录
    if author:
        cursor.execute("""
            SELECT 
                changed_revision,
                MIN(changed_date),
                changed_author,
                COUNT(*) as file_count
            FROM NODES
            WHERE wc_id = 1 AND op_depth = 0
                AND changed_author LIKE ?
            GROUP BY changed_revision
            ORDER BY changed_revision DESC
        """, (f'%{author}%',))
    else:
        cursor.execute("""
            SELECT 
                changed_revision,
                MIN(changed_date),
                changed_author,
                COUNT(*) as file_count
            FROM NODES
            WHERE wc_id = 1 AND op_depth = 0
            GROUP BY changed_revision
            ORDER BY changed_revision DESC
        """)
    
    print("修订版本列表:")
    print("-" * 80)
    
    total_files = 0
    for rev, date_ts, author_name, file_count in cursor.fetchall():
        date = datetime.utcfromtimestamp(date_ts / 1000000)
        total_files += file_count
        
        print(f"r{rev} | {date.strftime('%Y-%m-%d %H:%M')} | {author_name} | {file_count} 个文件")
        
        # 获取该修订版本修改的文件列表
        cursor.execute("""
            SELECT local_relpath, kind
            FROM NODES
            WHERE wc_id = 1 AND op_depth = 0
                AND changed_revision = ?
            ORDER BY local_relpath
        """, (rev,))
        
        for path, kind in cursor.fetchall():
            icon = '📄' if kind == 'file' else '📁'
            print(f"  {icon} {path}")
        print()
    
    print("=" * 80)
    print(f"统计: {total_files} 个文件, {cursor.rowcount} 个修订版本")
    print("=" * 80)
    
    conn.close()

if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else ".svn/wc.db"
    author = sys.argv[2] if len(sys.argv) > 2 else None
    generate_svn_report(db_path, author)
```

## 限制说明

### 本地数据库无法获取的信息

1. **提交日志（commit message）**: 存储在服务器端
2. **完整提交历史**: 只能看到工作副本更新的版本
3. **已删除的历史版本**: 本地数据库只存储当前状态
4. **其他分支**: 只能看到当前分支的信息

### 如何获取完整信息

要获取提交日志和完整历史，需要：

1. **安装 SVN 命令行工具**: SlikSVN, VisualSVN
2. **提供认证信息**: 用户名和密码
3. **使用 svn log 命令**: 
   ```bash
   svn log /path/to/project --limit 100 -v
   ```

## 与 Git 对照

| 功能 | Git (本地) | SVN (本地数据库) |
|------|------------|------------------|
| 提交历史 | ✅ 完整 | ⚠️ 仅更新版本 |
| 提交日志 | ✅ 完整 | ❌ 无法获取 |
| 作者信息 | ✅ 完整 | ✅ 最后修改者 |
| 时间信息 | ✅ 完整 | ✅ 最后修改时间 |
| 文件列表 | ✅ 完整 | ✅ 当前状态 |
| 无需网络 | ✅ | ✅ |

## 最佳实践

1. **定期更新工作副本**: 保持数据库最新
2. **结合服务器日志**: 本地 + 服务器信息互补
3. **导出报告存档**: 定期导出并保存历史记录
4. **使用版本号追踪**: 通过 revision 号关联服务器日志