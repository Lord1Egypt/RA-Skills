#!/usr/bin/env python3
"""
达梦数据库开发工具 v3.0
为昌叔量身定制的达梦数据库开发、审查和优化工具

功能:
  analyze    - 分析SQL语句，识别达梦兼容性问题
  optimize   - 优化SQL语句（字符串连接||、索引建议等）
  convert    - SQL Server语法转达梦语法（集成dm_converter）
  check      - 检查SQL文件的达梦兼容性（批量）
  procedure  - 生成达梦存储过程模板
  function   - 生成达梦函数模板
  trigger    - 生成达梦触发器模板
  test connect - 测试达梦数据库连接（需要dmPython）
  sql format - 格式化SQL（关键字大写、缩进）
  search     - 按标签搜索知识库（基于YAML frontmatter）
"""

import re
import sys
import os
import glob
from typing import List, Dict, Optional
from datetime import datetime


class DamengDatabaseTool:
    """达梦数据库专用工具"""

    # SQL Server → 达梦 数据类型映射
    TYPE_MAPPINGS = {
        'bit': 'BOOLEAN',
        'tinyint': 'SMALLINT',
        'smallint': 'SMALLINT',
        'int': 'INTEGER',
        'integer': 'INTEGER',
        'bigint': 'BIGINT',
        'decimal': 'DECIMAL',
        'numeric': 'NUMERIC',
        'float': 'DOUBLE',
        'real': 'REAL',
        'money': 'DECIMAL(19,4)',
        'smallmoney': 'DECIMAL(10,4)',
        'datetime': 'TIMESTAMP',
        'datetime2': 'TIMESTAMP',
        'smalldatetime': 'TIMESTAMP',
        'date': 'DATE',
        'time': 'TIME',
        'char': 'CHAR',
        'varchar': 'VARCHAR',
        'nchar': 'CHAR',
        'nvarchar': 'VARCHAR',
        'text': 'TEXT',
        'ntext': 'TEXT',
        'binary': 'BINARY',
        'varbinary': 'VARBINARY',
        'image': 'BLOB',
        'uniqueidentifier': 'VARCHAR(36)',
        'xml': 'TEXT',
        'sysname': 'VARCHAR(128)',
        'rowversion': 'BIGINT',
        'timestamp': 'BIGINT',
    }

    # 达梦常见坑模式（15种）
    COMMON_PITFALLS = {
        "string_concat": {
            "pattern": r"['\"]+\s*\+\s*['\"]+|@\w+\s*\+\s*['\"]|['\"]+\s*\+\s*@\w+",
            "description": "字符串连接使用+号",
            "solution": "达梦字符串连接应使用 || 而不是 +",
            "example": "SELECT 'Hello' || 'World' FROM dual",
            "severity": "error"
        },
        "date_format_mismatch": {
            "pattern": r"TO_CHAR\s*\([^,]+,\s*['\"]YYYY-MM-DD['\"]",
            "description": "TO_CHAR日期格式可能与目标字段不匹配",
            "solution": "TO_CHAR的日期格式必须与目标字段格式一致（如VARCHAR字段存YYYYMMDD则用'YYYYMMDD'）",
            "example": "TO_CHAR(sysdate, 'YYYYMMDD') 匹配 VARCHAR(YYYYMMDD)",
            "severity": "warning"
        },
        "calendar_cast_join": {
            "pattern": r"JOIN\s+\w*[Cc]alendar\w*\s+\w*\s+ON\s+.*CAST",
            "description": "Calendar表JOIN条件使用CAST",
            "solution": "Calendar表Date字段若为VARCHAR，JOIN条件也应用TO_CHAR匹配而非CAST",
            "example": "JOIN Calendar c ON TO_CHAR(t.date_col, 'YYYYMMDD') = c.Date",
            "severity": "warning"
        },
        "gtt_drop_create": {
            "pattern": r"DROP\s+TABLE\s+.*(?:GTT|#\w+)\s*;.*CREATE\s+TABLE",
            "description": "GTT/临时表反复DROP/CREATE",
            "solution": "不建议在存储过程中反复DROP/CREATE GTT，使用TRUNCATE或直接INSERT",
            "example": "TRUNCATE TABLE #temp; INSERT INTO #temp SELECT ...",
            "severity": "warning"
        },
        "select_star": {
            "pattern": r"SELECT\s+\*\s+FROM",
            "description": "使用SELECT *",
            "solution": "明确指定需要的列，避免SELECT *",
            "example": "SELECT col1, col2 FROM table_name",
            "severity": "performance"
        },
        "delete_no_where": {
            "pattern": r"DELETE\s+FROM\s+\w+\s*;",
            "description": "DELETE语句缺少WHERE条件",
            "solution": "添加WHERE条件，避免删除全部数据",
            "example": "DELETE FROM table_name WHERE condition",
            "severity": "danger"
        },
        "update_no_where": {
            "pattern": r"UPDATE\s+\w+\s+SET\s+.*;",
            "description": "UPDATE语句可能缺少WHERE条件",
            "solution": "确认WHERE条件存在，避免全表更新",
            "example": "UPDATE table_name SET col=val WHERE condition",
            "severity": "danger"
        },
        "in_subquery": {
            "pattern": r"WHERE\s+.*\bIN\s*\(\s*SELECT\b",
            "description": "使用IN子查询",
            "solution": "考虑使用EXISTS或JOIN替代IN子查询",
            "example": "WHERE EXISTS (SELECT 1 FROM t2 WHERE t2.id = t1.id)",
            "severity": "performance"
        },
        "non_sargable": {
            "pattern": r"WHERE\s+.*(?:UPPER|LOWER|SUBSTR|REPLACE|TRIM)\s*\(",
            "description": "WHERE条件中对列使用函数（非SARG）",
            "solution": "避免在WHERE条件中对列使用函数，会导致索引失效",
            "example": "改为: WHERE name LIKE 'ABC%' 替代 WHERE UPPER(name) = 'ABC'",
            "severity": "performance"
        },
        "getdate": {
            "pattern": r"\bGETDATE\s*\(",
            "description": "使用SQL Server的GETDATE()",
            "solution": "达梦使用CURRENT_TIMESTAMP或SYSDATE",
            "example": "SELECT CURRENT_TIMESTAMP FROM dual",
            "severity": "error"
        },
        "isnull": {
            "pattern": r"\bISNULL\s*\(",
            "description": "使用SQL Server的ISNULL()",
            "solution": "达梦使用NVL()",
            "example": "SELECT NVL(col, 0) FROM table_name",
            "severity": "error"
        },
        "top_clause": {
            "pattern": r"\bTOP\s+\d+",
            "description": "使用SQL Server的TOP子句",
            "solution": "达梦使用FETCH FIRST N ROWS ONLY或ROWNUM",
            "example": "SELECT * FROM t FETCH FIRST 10 ROWS ONLY",
            "severity": "error"
        },
        "identity_insert": {
            "pattern": r"\bIDENTITY\s*\(",
            "description": "使用SQL Server的IDENTITY",
            "solution": "达梦使用IDENTITY(1,1)或SEQUENCE",
            "example": "CREATE TABLE t (id INT IDENTITY(1,1), name VARCHAR(100))",
            "severity": "warning"
        },
        "nolock_hint": {
            "pattern": r"WITH\s*\(\s*NOLOCK\s*\)",
            "description": "使用SQL Server的NOLOCK提示",
            "solution": "达梦不支持WITH(NOLOCK)，移除或改用SET TRANSACTION ISOLATION LEVEL",
            "example": "移除 WITH(NOLOCK)，或使用 SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED",
            "severity": "error"
        },
        "datediff_only_day": {
            "pattern": r"\bDATEDIFF\s*\(\s*day\s*,",
            "description": "DATEDIFF(day,...)在达梦中的处理",
            "solution": "达梦可用 (end_date - start_date) 计算天数差",
            "example": "SELECT (end_date - start_date) FROM dual",
            "severity": "warning"
        }
    }

    # SQL关键字大写列表（用于格式化）
    SQL_KEYWORDS = [
        'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'IN', 'EXISTS',
        'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE',
        'CREATE', 'ALTER', 'DROP', 'TABLE', 'INDEX', 'VIEW', 'SEQUENCE',
        'PROCEDURE', 'FUNCTION', 'TRIGGER', 'PACKAGE',
        'AS', 'IS', 'BEGIN', 'END', 'DECLARE', 'IF', 'ELSE', 'ELSIF',
        'WHILE', 'FOR', 'LOOP', 'EXIT', 'WHEN', 'THEN', 'RETURN',
        'ORDER', 'BY', 'GROUP', 'HAVING', 'UNION', 'ALL', 'INTERSECT',
        'MINUS', 'EXCEPT', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL',
        'OUTER', 'CROSS', 'ON', 'USING', 'BETWEEN', 'LIKE', 'CASCADED',
        'NULL', 'ISNULL', 'NVL', 'DISTINCT', 'UNIQUE', 'PRIMARY',
        'KEY', 'FOREIGN', 'REFERENCES', 'CHECK', 'DEFAULT', 'CONSTRAINT',
        'COMMIT', 'ROLLBACK', 'SAVEPOINT', 'GRANT', 'REVOKE',
        'CASE', 'WHEN', 'CAST', 'CONVERT', 'COALESCE', 'DECODE',
        'COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'ROW_NUMBER', 'RANK',
        'DENSE_RANK', 'OVER', 'PARTITION', 'FETCH', 'FIRST', 'ROWS',
        'ONLY', 'NEXT', 'LIMIT', 'OFFSET', 'ASC', 'DESC',
        'CURSOR', 'OPEN', 'CLOSE', 'FETCH', 'FOUND', 'NOTFOUND',
        'EXCEPTION', 'OTHERS', 'RAISE', 'RAISE_APPLICATION_ERROR',
        'SQLCODE', 'SQLERRM', 'DBMS_OUTPUT', 'PUT_LINE',
        'CURRENT_TIMESTAMP', 'SYSDATE', 'DUAL',
        'OR', 'REPLACE', 'EACH', 'ROW', 'AFTER', 'BEFORE',
        'REFERENCES', 'IDENTITY', 'INCREMENT', 'START', 'WITH',
        'COLUMN', 'ADD', 'MODIFY', 'RENAME', 'COMMENT', 'TABLESPACE',
        'INTEGER', 'BIGINT', 'SMALLINT', 'NUMERIC', 'DECIMAL',
        'VARCHAR', 'CHAR', 'TEXT', 'BLOB', 'CLOB', 'BOOLEAN',
        'DATE', 'TIME', 'TIMESTAMP', 'REAL', 'DOUBLE', 'FLOAT',
        'PRECISION', 'SCALE', 'VARYING', 'CHARACTER',
        'BOOLEAN', 'TRUE', 'FALSE',
        'TRUNCATE', 'MERGE', 'MATCHED',
        'MATERIALIZED', 'REFRESH', 'COMPLETE', 'FAST',
        'ENABLE', 'DISABLE', 'VISIBLE', 'INVISIBLE',
        'ANALYZE', 'COMPUTE', 'STATISTICS',
        'SHOW', 'TABLES', 'SCHEMA', 'DATABASE',
        'LIKE', 'ILIKE', 'SIMILAR', 'TO', 'ESCAPE',
        'ANY', 'SOME', 'NO', 'WAIT', 'NOWAIT', 'SKIP',
        'LOCK', 'MODE', 'SHARE', 'EXCLUSIVE', 'ROWLOCK',
        'PRESERVE', 'ROWS', 'VALIDATE', 'NOVALIDATE',
        'RELY', 'NORELY', 'DEFERRABLE', 'DEFERRED', 'IMMEDIATE',
        'INITIALLY', 'ENABLE', 'DISABLE',
        'FOR', 'PERCENT', 'TOP', 'OUTPUT', 'INSERTED',
        'LOGGED', 'UNLOGGED', 'TEMP', 'TEMPORARY', 'GLOBAL',
        'LOCAL', 'SESSION', 'TRANSACTION', 'ISOLATION', 'LEVEL',
        'READ', 'COMMITTED', 'SERIALIZABLE', 'REPEATABLE',
        'CONCURRENTLY', 'CONNECTION', 'DISCONNECT', 'CONNECT',
    ]

    def __init__(self):
        self.dm_converter = None  # 延迟加载

    def _load_converter(self):
        """延迟加载dm_converter（可选依赖，路径: ~/.hermes/skills/sql-splitter/scripts/）"""
        if self.dm_converter is not None:
            return True
        try:
            converter_path = os.path.expanduser(
                "~/.hermes/skills/sql-splitter/scripts/dm_converter.py"
            )
            if os.path.exists(converter_path):
                sys.path.insert(0, os.path.dirname(converter_path))
                from dm_converter import DMConverter
                self.dm_converter = DMConverter()
                return True
        except Exception as e:
            print(f"[警告] 无法加载dm_converter: {e}")
        return False

    # ---------------------------------------------------------------
    # 核心分析功能
    # ---------------------------------------------------------------

    def analyze_sql(self, sql: str) -> Dict:
        """分析SQL语句，识别达梦兼容性和性能问题"""
        issues = []

        for issue_name, issue_info in self.COMMON_PITFALLS.items():
            matches = re.findall(issue_info["pattern"], sql, re.IGNORECASE | re.DOTALL)
            if matches:
                issues.append({
                    "type": issue_name,
                    "severity": issue_info.get("severity", "warning"),
                    "description": issue_info["description"],
                    "solution": issue_info["solution"],
                    "example": issue_info["example"],
                    "count": len(matches)
                })

        # 按严重等级分类统计
        by_severity = {}
        for issue in issues:
            sev = issue["severity"]
            by_severity[sev] = by_severity.get(sev, 0) + 1

        return {
            "issues": issues,
            "summary": f"发现 {len(issues)} 个问题",
            "by_severity": by_severity
        }

    def check_file(self, filepath: str) -> Dict:
        """检查SQL文件的达梦兼容性"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                sql = f.read()
        except FileNotFoundError:
            return {"error": f"文件不存在: {filepath}"}
        except Exception as e:
            return {"error": f"读取文件失败: {e}"}

        result = self.analyze_sql(sql)
        result["file"] = filepath
        result["line_count"] = sql.count('\n') + 1
        return result

    # ---------------------------------------------------------------
    # SQL优化
    # ---------------------------------------------------------------

    def optimize_sql(self, sql: str) -> str:
        """优化SQL语句，做达梦兼容转换

        处理的转换:
        1. 字符串字面量之间的 + → ||  (如 'a' + 'b' → 'a' || 'b')
        2. 字符串字面量与变量之间的 + → ||  (如 'a' + @var → 'a' || @var)
        3. 变量与字符串字面量之间的 + → ||  (如 @var + 'a' → @var || 'a')
        4. GETDATE() → CURRENT_TIMESTAMP
        5. ISNULL → NVL
        6. TOP N → FETCH FIRST N ROWS ONLY
        7. WITH(NOLOCK) → 移除
        8. 索引建议
        """
        optimized = sql

        # 替换1: 字符串字面量之间的 + → ||
        # 匹配: 'str1' + 'str2'  →  'str1' || 'str2'
        optimized = re.sub(
            r"('[^']*')\s*\+\s*('[^']*')",
            r'\1 || \2',
            optimized
        )

        # 替换2: 字符串字面量 + 变量 → 字符串 || 变量
        # 匹配: 'str' + @var  →  'str' || @var
        optimized = re.sub(
            r"('[^']*')\s*\+\s*(@\w+)",
            r'\1 || \2',
            optimized
        )

        # 替换3: 变量 + 字符串字面量 → 变量 || 字符串字面量
        # 匹配: @var + 'str'  →  @var || 'str'
        optimized = re.sub(
            r"(@\w+)\s*\+\s*('[^']*')",
            r'\1 || \2',
            optimized
        )

        # 替换4: 也处理双引号字符串的拼接（较少见但完整覆盖）
        optimized = re.sub(
            r'("[^"]*")\s*\+\s*("[^"]*")',
            r'\1 || \2',
            optimized
        )
        optimized = re.sub(
            r'("[^"]*")\s*\+\s*(@\w+)',
            r'\1 || \2',
            optimized
        )
        optimized = re.sub(
            r"(@\w+)\s*\+\s*(\"[^\"]*\")",
            r'\1 || \2',
            optimized
        )

        # GETDATE() → CURRENT_TIMESTAMP
        optimized = re.sub(r'\bGETDATE\s*\(\s*\)', 'CURRENT_TIMESTAMP', optimized, flags=re.IGNORECASE)

        # ISNULL → NVL
        optimized = re.sub(r'\bISNULL\s*\(', 'NVL(', optimized, flags=re.IGNORECASE)

        # TOP N → FETCH FIRST N ROWS ONLY
        def replace_top(m):
            n = m.group(1)
            return f'/* TOP {n} → */ FETCH FIRST {n} ROWS ONLY'
        optimized = re.sub(r'\bTOP\s+(\d+)', replace_top, optimized, flags=re.IGNORECASE)

        # WITH(NOLOCK) → 移除
        optimized = re.sub(r'\bWITH\s*\(\s*NOLOCK\s*\)', '', optimized, flags=re.IGNORECASE)

        # 索引建议
        if 'WHERE' in optimized.upper() and 'INDEX' not in optimized.upper():
            optimized += "\n-- [建议] 为WHERE条件中的列创建索引"

        return optimized

    # ---------------------------------------------------------------
    # SQL Server → 达梦 转换（集成dm_converter）
    # ---------------------------------------------------------------

    def convert_sqlserver_to_dm(self, sql: str, conversion_type: str = 'generic') -> Dict:
        """将SQL Server语法转换为达梦语法（集成dm_converter）

        路径: ~/.hermes/skills/sql-splitter/scripts/dm_converter.py
        """
        if not self._load_converter():
            return {
                "error": "dm_converter不可用，请确认 ~/.hermes/skills/sql-splitter/scripts/dm_converter.py 存在",
                "fallback": self.optimize_sql(sql)
            }

        try:
            result = self.dm_converter.convert(sql, conversion_type)
            return {
                "converted": result.converted,
                "changes": result.changes,
                "change_count": len(result.changes)
            }
        except Exception as e:
            return {
                "error": f"转换失败: {e}",
                "fallback": self.optimize_sql(sql)
            }

    # ---------------------------------------------------------------
    # 知识库标签搜索（基于YAML frontmatter）
    # ---------------------------------------------------------------

    def search_by_tags(self, tags: List[str], search_dir: str = None) -> List[Dict]:
        """根据标签搜索.md文件，基于YAML frontmatter中的tags字段做匹配

        Args:
            tags: 要搜索的标签列表
            search_dir: 搜索目录（默认: ~/wiki）

        Returns:
            匹配的文件列表，每项包含 file, title, tags, match_count, preview
        """
        if search_dir is None:
            search_dir = os.path.expanduser("~/wiki")

        if not os.path.isdir(search_dir):
            return []

        results = []
        tags_lower = [t.lower() for t in tags]

        for root, dirs, files in os.walk(search_dir):
            # 跳过隐藏目录
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for filename in files:
                if not filename.endswith('.md'):
                    continue
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception:
                    continue

                # 解析YAML frontmatter
                frontmatter = self._parse_frontmatter(content)
                if not frontmatter:
                    continue

                file_tags = frontmatter.get('tags', [])
                if not file_tags:
                    continue

                # 如果file_tags是字符串（YAML的单行写法如 tags: [a, b, c]），尝试拆分
                if isinstance(file_tags, str):
                    file_tags = [t.strip().strip('[]') for t in file_tags.split(',')]

                # 匹配标签（不区分大小写）
                file_tags_lower = [t.lower() for t in file_tags]
                matched_tags = [t for t in tags_lower if t in file_tags_lower]

                if matched_tags:
                    # 提取标题（优先用frontmatter的title，否则用文件名）
                    title = frontmatter.get('title', os.path.splitext(filename)[0])
                    # 提取预览内容（去掉frontmatter后的前200字符）
                    preview = self._get_content_preview(content, max_len=200)

                    results.append({
                        "file": filepath,
                        "title": str(title),
                        "tags": file_tags,
                        "match_count": len(matched_tags),
                        "matched_tags": matched_tags,
                        "preview": preview
                    })

        # 按匹配数量降序排列
        results.sort(key=lambda x: x["match_count"], reverse=True)
        return results

    def _parse_frontmatter(self, content: str) -> Optional[Dict]:
        """解析Markdown文件中的YAML frontmatter

        支持 --- 分隔的标准frontmatter格式:
        ---
        title: 文档标题
        tags: [tag1, tag2, tag3]
        ---
        """
        # 匹配 --- 开头和结尾的frontmatter
        fm_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n?', re.DOTALL)
        match = fm_pattern.match(content)
        if not match:
            return None

        fm_text = match.group(1)
        result = {}

        for line in fm_text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' not in line:
                continue

            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()

            # 解析 tags 字段
            if key == 'tags':
                # 支持多种格式:
                # tags: [tag1, tag2]
                # tags:
                #   - tag1
                #   - tag2
                # tags: tag1, tag2
                if value.startswith('[') and value.endswith(']'):
                    # YAML行内列表: [tag1, tag2, tag3]
                    value = value[1:-1]
                    result['tags'] = [t.strip().strip("'\"") for t in value.split(',') if t.strip()]
                elif not value:
                    # 多行列表（下一行开始 - ），收集后续行
                    tag_list = []
                    fm_lines = fm_text.split('\n')
                    in_tags = False
                    for fl in fm_lines:
                        fl_stripped = fl.strip()
                        if fl_stripped.startswith('tags:'):
                            in_tags = True
                            continue
                        if in_tags:
                            if fl_stripped.startswith('- '):
                                tag_list.append(fl_stripped[2:].strip().strip("'\""))
                            elif fl_stripped and not fl_stripped.startswith('#'):
                                break
                    result['tags'] = tag_list
                else:
                    # 逗号分隔: tags: tag1, tag2
                    result['tags'] = [t.strip().strip("'\"") for t in value.split(',') if t.strip()]
            else:
                # 简单键值对
                result[key] = value.strip("'\"")

        return result if result else None

    def _get_content_preview(self, content: str, max_len: int = 200) -> str:
        """获取去掉frontmatter后的内容预览"""
        # 去除frontmatter
        fm_pattern = re.compile(r'^---\s*\n.*?\n---\s*\n?', re.DOTALL)
        body = fm_pattern.sub('', content).strip()
        # 去除多余空白
        body = re.sub(r'\n{2,}', '\n\n', body)
        if len(body) > max_len:
            return body[:max_len] + '...'
        return body

    # ---------------------------------------------------------------
    # 模板生成
    # ---------------------------------------------------------------

    def generate_procedure_template(self, name: str, params: List[Dict] = None,
                                     with_logging: bool = True, with_exception: bool = True) -> str:
        """生成达梦存储过程模板

        Args:
            name: 存储过程名称
            params: 参数列表 [{"name": "p_date", "type": "DATE", "mode": "IN"}, ...]
            with_logging: 是否包含日志记录
            with_exception: 是否包含异常处理
        """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 参数定义
        if params:
            param_lines = []
            for p in params:
                pname = p.get("name", "p_param")
                ptype = p.get("type", "VARCHAR(100)")
                pmode = p.get("mode", "IN")
                param_lines.append(f"    {pmode} {pname} {ptype}")
            param_str = ",\n".join(param_lines)
        else:
            param_str = "    -- IN p_param VARCHAR(100)  -- 参数定义"

        # 日志记录段
        logging_block = ""
        if with_logging:
            logging_block = """
    -- 记录开始时间
    v_start_time := CURRENT_TIMESTAMP;
    v_proc_name := '{name}';
    -- 如有日志表: INSERT INTO proc_log(proc_name, start_time, params) VALUES(v_proc_name, v_start_time, ...);
""".format(name=name)

        # 异常处理段
        exception_block = ""
        if with_exception:
            exception_block = """
    EXCEPTION
        WHEN OTHERS THEN
            v_err_code := SQLCODE;
            v_err_msg  := SQLERRM;
            -- 记录错误日志
            -- INSERT INTO proc_error_log(proc_name, error_code, error_msg, error_time)
            --     VALUES('{name}', v_err_code, v_err_msg, CURRENT_TIMESTAMP);
            -- 根据业务需要选择: 重新抛出异常 或 记录后继续
            RAISE;
""".format(name=name)

        template = f"""-- ============================================================
-- 存储过程: {name}
-- 创建时间: {now}
-- 说明: {name}的存储过程
-- ============================================================

CREATE OR REPLACE PROCEDURE {name}(
{param_str}
)
AS
    -- 变量声明
    v_result      VARCHAR(4000);
    v_count       INT;
    v_start_time  TIMESTAMP;
    v_proc_name   VARCHAR(100);
    v_err_code    INT;
    v_err_msg     VARCHAR(4000);
BEGIN
{logging_block}
    -- 主要业务逻辑
    BEGIN
        -- TODO: 在这里编写主要逻辑

        -- 示例: 查询数据
        SELECT COUNT(*)
        INTO v_count
        FROM your_table
        WHERE condition = 'value';

        -- 示例: 条件处理
        IF v_count > 0 THEN
            v_result := '成功处理 ' || v_count || ' 条记录';
            -- DBMS_OUTPUT.PUT_LINE(v_result);
        ELSE
            v_result := '没有找到匹配的记录';
        END IF;
{exception_block}
    END;

    -- 记录结束时间
    -- v_end_time := CURRENT_TIMESTAMP;
    -- DBMS_OUTPUT.PUT_LINE(v_proc_name || ' 完成, 耗时: ' || (v_end_time - v_start_time));

END {name};
/
"""
        return template

    def generate_function_template(self, name: str, return_type: str = "VARCHAR(4000)",
                                    params: List[Dict] = None) -> str:
        """生成达梦函数模板

        Args:
            name: 函数名称
            return_type: 返回值类型
            params: 参数列表
        """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if params:
            param_lines = []
            for p in params:
                pname = p.get("name", "p_param")
                ptype = p.get("type", "VARCHAR(100)")
                param_lines.append(f"    {pname} {ptype}")
            param_str = ",\n".join(param_lines)
        else:
            param_str = "    -- p_param VARCHAR(100)  -- 参数定义"

        template = f"""-- ============================================================
-- 函数: {name}
-- 创建时间: {now}
-- 返回类型: {return_type}
-- 说明: {name}的函数
-- ============================================================

CREATE OR REPLACE FUNCTION {name}(
{param_str}
)
RETURN {return_type}
AS
    -- 变量声明
    v_result  {return_type};
    v_count   INT;
BEGIN
    -- TODO: 在这里编写函数逻辑

    -- 示例: 查询并返回结果
    SELECT COUNT(*)
    INTO v_count
    FROM your_table
    WHERE condition = 'value';

    v_result := '处理了 ' || v_count || ' 条记录';

    RETURN v_result;

EXCEPTION
    WHEN OTHERS THEN
        -- 异常时返回错误信息
        RETURN 'ERROR: ' || SQLERRM;
END {name};
/
"""
        return template

    def generate_trigger_template(self, name: str, table_name: str,
                                   trigger_type: str = "AFTER INSERT") -> str:
        """生成达梦触发器模板

        Args:
            name: 触发器名称
            table_name: 表名
            trigger_type: 触发类型 (AFTER INSERT / AFTER UPDATE / BEFORE INSERT 等)
        """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 解析触发类型
        timing = "AFTER"
        event = "INSERT"
        if trigger_type.upper().startswith("BEFORE"):
            timing = "BEFORE"
            event = trigger_type.upper().replace("BEFORE", "").strip() or "INSERT"
        elif trigger_type.upper().startswith("AFTER"):
            timing = "AFTER"
            event = trigger_type.upper().replace("AFTER", "").strip() or "INSERT"

        # 达梦触发器中引用NEW/OLD
        ref_var = "NEW" if event in ("INSERT", "UPDATE") else "OLD"

        template = f"""-- ============================================================
-- 触发器: {name}
-- 表: {table_name}
-- 类型: {timing} {event}
-- 创建时间: {now}
-- 说明: {table_name}表{timing} {event}时触发
-- ============================================================

CREATE OR REPLACE TRIGGER {name}
{timing} {event} ON {table_name}
FOR EACH ROW
AS
    -- 变量声明
    v_result  VARCHAR(4000);
BEGIN
    -- TODO: 在这里编写触发器逻辑

    -- 示例: 访问新插入/更新的值
    -- :{ref_var}.column_name  -- 引用{event}时的列值

    -- 示例: 记录操作日志
    -- INSERT INTO operation_log(table_name, operation, operator, operate_time)
    --     VALUES('{table_name}', '{event}', USER, CURRENT_TIMESTAMP);

    -- 示例: 数据校验
    -- IF :{ref_var}.status IS NULL THEN
    --     RAISE_APPLICATION_ERROR(-20001, 'status不能为空');
    -- END IF;

EXCEPTION
    WHEN OTHERS THEN
        -- 触发器中的异常处理
        -- 注意: 触发器中的异常会回滚整个DML操作
        RAISE_APPLICATION_ERROR(-20002, '触发器{name}执行失败: ' || SQLERRM);
END {name};
/
"""
        return template

    # ---------------------------------------------------------------
    # SQL格式化
    # ---------------------------------------------------------------

    def format_sql(self, sql: str) -> str:
        """格式化SQL：关键字大写、缩进

        Returns:
            格式化后的SQL字符串
        """
        # 构建关键字匹配的正则（按长度降序，优先匹配长关键字）
        keywords_sorted = sorted(set(self.SQL_KEYWORDS), key=len, reverse=True)
        keyword_pattern = '|'.join(re.escape(kw) for kw in keywords_sorted)

        # 将SQL按字符串字面量和非字符串部分分开处理，避免误替换字符串内的关键字
        parts = self._split_sql_preserving_strings(sql)

        result_parts = []
        for part_type, part_text in parts:
            if part_type == 'string':
                # 字符串字面量，保持原样
                result_parts.append(part_text)
            elif part_type == 'comment':
                # 注释，保持原样
                result_parts.append(part_text)
            else:
                # 非字符串部分：关键字大写
                uppered = re.sub(
                    r'\b(' + keyword_pattern + r')\b',
                    lambda m: m.group(1).upper(),
                    part_text,
                    flags=re.IGNORECASE
                )
                result_parts.append(uppered)

        formatted = ''.join(result_parts)

        # 缩进处理: 主要关键字换行并缩进子句
        indent_rules = [
            # 子句级别关键字前换行
            (r'\bFROM\b', '\nFROM '),
            (r'\bWHERE\b', '\nWHERE '),
            (r'\bGROUP\s+BY\b', '\nGROUP BY '),
            (r'\bHAVING\b', '\nHAVING '),
            (r'\bORDER\s+BY\b', '\nORDER BY '),
            (r'\bLIMIT\b', '\nLIMIT '),
            (r'\bFETCH\s+FIRST\b', '\nFETCH FIRST '),
            (r'\bUNION\b', '\nUNION '),
            (r'\bINTERSECT\b', '\nINTERSECT '),
            (r'\bMINUS\b', '\nMINUS '),
            (r'\bEXCEPT\b', '\nEXCEPT '),
            # JOIN 关键字
            (r'\bINNER\s+JOIN\b', '\nINNER JOIN '),
            (r'\bLEFT\s+(?:OUTER\s+)?JOIN\b', '\nLEFT JOIN '),
            (r'\bRIGHT\s+(?:OUTER\s+)?JOIN\b', '\nRIGHT JOIN '),
            (r'\bFULL\s+(?:OUTER\s+)?JOIN\b', '\nFULL JOIN '),
            (r'\bCROSS\s+JOIN\b', '\nCROSS JOIN '),
            (r'\bJOIN\b', '\nJOIN '),
            # 逻辑连接词换行（缩进）
            (r'\bAND\b', '\n  AND '),
            (r'\bOR\b', '\n  OR '),
            # SET 关键字
            (r'\bSET\b', '\nSET '),
        ]

        # 只对SELECT/UPDATE/DELETE等语句格式化
        upper_check = formatted.strip().upper()
        if upper_check.startswith(('SELECT', 'UPDATE', 'DELETE', 'WITH', 'INSERT')):
            for pattern, replacement in indent_rules:
                formatted = re.sub(pattern, replacement, formatted, flags=re.IGNORECASE)

        # 清理多余空行
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)
        return formatted.strip()

    def _split_sql_preserving_strings(self, sql: str) -> List[tuple]:
        """将SQL拆分为字符串字面量、注释和普通代码部分

        Returns:
            列表，每项为 (type, text)，type为 'string'/'comment'/'code'
        """
        parts = []
        # 匹配字符串字面量('...')和行注释(--...)和块注释(/*...*/)
        pattern = re.compile(
            r"('[^']*(?:''[^']*)*')"    # 单引号字符串（支持转义''）
            r"|(/\*[\s\S]*?\*/)"        # 块注释 /* ... */
            r"|(--[^\n]*)",              # 行注释 -- ...
            re.DOTALL
        )

        last_end = 0
        for match in pattern.finditer(sql):
            # 添加匹配前的普通代码
            if match.start() > last_end:
                parts.append(('code', sql[last_end:match.start()]))

            if match.group(1):
                parts.append(('string', match.group(1)))
            elif match.group(2):
                parts.append(('comment', match.group(2)))
            elif match.group(3):
                parts.append(('comment', match.group(3)))

            last_end = match.end()

        # 添加最后的普通代码
        if last_end < len(sql):
            parts.append(('code', sql[last_end:]))

        return parts if parts else [('code', sql)]

    # ---------------------------------------------------------------
    # 数据库连接测试
    # ---------------------------------------------------------------

    def test_connect(self, host: str = 'localhost', port: int = 5236,
                     user: str = '', password: str = '',
                     schema: str = None) -> Dict:
        """测试达梦数据库连接（需要dmPython，可选依赖）

        Args:
            host: 数据库主机地址
            port: 端口号（达梦默认5236）
            user: 用户名
            password: 密码
            schema: 目标SCHEMA（可选）

        Returns:
            包含连接状态和基本信息的字典
        """
        if not user or not password:
            return {
                "host": host, "port": port, "user": user,
                "connected": False,
                "server_info": None,
                "error": "请提供用户名和密码: test connect <host> <port> <user> <password>"
            }

        result = {
            "host": host,
            "port": port,
            "user": user,
            "connected": False,
            "server_info": None,
            "error": None
        }

        try:
            import dmPython
        except ImportError:
            result["error"] = (
                "dmPython未安装。安装方法: pip install dmPython\n"
                "注意: dmPython需要达梦客户端库(dmcltxxx)，详情参考达梦官方文档"
            )
            return result

        conn = None
        cursor = None
        try:
            # 尝试连接
            conn = dmPython.connect(
                user=user,
                password=password,
                server=host,
                port=port
            )

            result["connected"] = True
            cursor = conn.cursor()

            # 切换SCHEMA（如果指定）
            if schema:
                cursor.execute(f"SET SCHEMA {schema}")

            # 获取服务器版本信息
            try:
                cursor.execute("SELECT * FROM V$VERSION")
                version_rows = cursor.fetchall()
                if version_rows:
                    result["server_info"] = "; ".join(str(r[0]) for r in version_rows)
            except Exception:
                try:
                    cursor.execute("SELECT ID_CODE FROM V$INSTANCE")
                    instance_rows = cursor.fetchall()
                    if instance_rows:
                        result["server_info"] = str(instance_rows[0][0])
                except Exception:
                    result["server_info"] = "已连接（无法获取版本信息）"

            # 获取当前SCHEMA
            try:
                cursor.execute("SELECT CURRENT_SCHEMA")
                schema_row = cursor.fetchone()
                if schema_row:
                    result["current_schema"] = str(schema_row[0])
            except Exception:
                pass

            # 获取当前时间（验证查询能力）
            try:
                cursor.execute("SELECT CURRENT_TIMESTAMP")
                ts_row = cursor.fetchone()
                if ts_row:
                    result["server_time"] = str(ts_row[0])
            except Exception:
                pass

        except Exception as e:
            result["connected"] = False
            result["error"] = f"连接失败: {e}"
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass

        return result

    # ---------------------------------------------------------------
    # 报告格式化
    # ---------------------------------------------------------------

    def format_analysis_report(self, result: Dict) -> str:
        """格式化分析报告"""
        lines = []
        lines.append("=" * 60)
        lines.append("  达梦数据库兼容性分析报告")
        lines.append("=" * 60)

        if "file" in result:
            lines.append(f"  文件: {result['file']}")
            lines.append(f"  行数: {result.get('line_count', '?')}")

        lines.append(f"  {result['summary']}")

        by_sev = result.get("by_severity", {})
        if by_sev:
            lines.append(
                f"  错误: {by_sev.get('error', 0)}  "
                f"警告: {by_sev.get('warning', 0)}  "
                f"性能: {by_sev.get('performance', 0)}  "
                f"危险: {by_sev.get('danger', 0)}"
            )

        lines.append("-" * 60)

        for i, issue in enumerate(result["issues"], 1):
            sev = issue.get("severity", "warning")
            sev_mark = {"error": "x", "warning": "!", "performance": "~", "danger": "!!!"}.get(sev, "?")
            lines.append(f"\n  [{sev_mark}] 问题{i}: {issue['description']}")
            lines.append(f"      解决: {issue['solution']}")
            lines.append(f"      示例: {issue['example']}")
            if issue.get("count", 1) > 1:
                lines.append(f"      出现次数: {issue['count']}")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)

    def format_search_results(self, results: List[Dict]) -> str:
        """格式化标签搜索结果"""
        if not results:
            return "未找到匹配的知识库文件"

        lines = []
        lines.append("=" * 60)
        lines.append(f"  标签搜索结果（共 {len(results)} 个文件）")
        lines.append("=" * 60)

        for i, item in enumerate(results, 1):
            lines.append(f"\n  [{i}] {item['title']}")
            lines.append(f"      文件: {item['file']}")
            lines.append(f"      标签: {', '.join(item['tags'])}")
            lines.append(f"      匹配数: {item['match_count']}  (匹配: {', '.join(item['matched_tags'])})")
            if item.get('preview'):
                preview = item['preview'].replace('\n', ' ')[:150]
                lines.append(f"      预览: {preview}...")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)

    def format_connect_result(self, result: Dict) -> str:
        """格式化连接测试结果"""
        lines = []
        lines.append("=" * 60)
        lines.append("  达梦数据库连接测试")
        lines.append("=" * 60)
        lines.append(f"  主机: {result['host']}:{result['port']}")
        lines.append(f"  用户: {result['user']}")

        if result["connected"]:
            lines.append(f"  状态: 连接成功")
            if result.get("server_info"):
                lines.append(f"  服务器: {result['server_info']}")
            if result.get("current_schema"):
                lines.append(f"  当前SCHEMA: {result['current_schema']}")
            if result.get("server_time"):
                lines.append(f"  服务器时间: {result['server_time']}")
        else:
            lines.append(f"  状态: 连接失败")
            if result.get("error"):
                lines.append(f"  错误: {result['error']}")

        lines.append("=" * 60)
        return "\n".join(lines)


# =================================================================
# 主函数
# =================================================================

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("达梦数据库开发工具 v3.0")
        print()
        print("使用方法:")
        print("  python dameng-tool.py analyze <sql_file>       分析SQL文件的达梦兼容性")
        print("  python dameng-tool.py optimize <sql_file>      优化SQL语句")
        print("  python dameng-tool.py convert <sql_file> [类型] SQL Server转达梦语法(需dm_converter)")
        print("  python dameng-tool.py check <dir_or_file>      批量检查兼容性")
        print("  python dameng-tool.py procedure <name> [参数]  生成存储过程模板")
        print("  python dameng-tool.py function <name> [返回类型] 生成函数模板")
        print("  python dameng-tool.py trigger <name> <表名> [类型] 生成触发器模板")
        print("  python dameng-tool.py test connect [host] [port] [user] [password]")
        print("      测试达梦数据库连接")
        print("  python dameng-tool.py sql format <sql_file>    格式化SQL(关键字大写、缩进)")
        print("  python dameng-tool.py search <tag1> [tag2] ... 按标签搜索知识库")
        print()
        print("示例:")
        print("  python dameng-tool.py analyze proc_sp_report.sql")
        print("  python dameng-tool.py convert proc_sp_report.sql")
        print("  python dameng-tool.py procedure sp_report")
        print("  python dameng-tool.py function fn_calc RETURN_TYPE")
        print("  python dameng-tool.py trigger trg_audit orders 'AFTER INSERT'")
        print("  python dameng-tool.py test connect <host> <port> <user> <password>")
        print("  python dameng-tool.py sql format my_query.sql")
        print("  python dameng-tool.py search investment stock")
        return

    command = sys.argv[1].lower()
    tool = DamengDatabaseTool()

    # --- analyze ---
    if command == 'analyze':
        if len(sys.argv) < 3:
            print("错误: 请指定SQL文件")
            return
        filepath = sys.argv[2]
        result = tool.check_file(filepath)
        if "error" in result:
            print(f"错误: {result['error']}")
        else:
            print(tool.format_analysis_report(result))

    # --- optimize ---
    elif command == 'optimize':
        if len(sys.argv) < 3:
            print("错误: 请指定SQL文件")
            return
        filepath = sys.argv[2]
        result = tool.check_file(filepath)
        if "error" in result:
            print(f"错误: {result['error']}")
            return
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                sql = f.read()
            optimized = tool.optimize_sql(sql)
            print("优化后的SQL:")
            print("-" * 60)
            print(optimized)
        except Exception as e:
            print(f"错误: {e}")

    # --- convert ---
    elif command == 'convert':
        if len(sys.argv) < 3:
            print("错误: 请指定SQL文件")
            return
        filepath = sys.argv[2]
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                sql = f.read()
            conv_type = sys.argv[3] if len(sys.argv) > 3 else 'generic'
            result = tool.convert_sqlserver_to_dm(sql, conv_type)
            if "error" in result:
                print(f"[警告] {result['error']}")
                print("使用基础优化:")
                print(result.get("fallback", sql))
            else:
                print(f"转换完成，共 {result['change_count']} 处修改:")
                print("-" * 60)
                print(result["converted"])
                if result["changes"]:
                    print("\n修改详情:")
                    for ch in result["changes"]:
                        print(f"  [{ch.get('desc', ch.get('type', '?'))}] {ch.get('old', '?')} -> {ch.get('new', '?')}")
        except Exception as e:
            print(f"错误: {e}")

    # --- check (批量) ---
    elif command == 'check':
        if len(sys.argv) < 3:
            print("错误: 请指定目录或文件")
            return
        target = sys.argv[2]
        if os.path.isfile(target):
            result = tool.check_file(target)
            if "error" in result:
                print(f"错误: {result['error']}")
            else:
                print(tool.format_analysis_report(result))
        elif os.path.isdir(target):
            sql_files = []
            for ext in ('*.sql', '*.SQL'):
                sql_files.extend(glob.glob(os.path.join(target, ext)))
            if not sql_files:
                print(f"目录 {target} 中没有SQL文件")
                return
            total_issues = 0
            for f in sorted(sql_files):
                result = tool.check_file(f)
                if "error" not in result:
                    n = len(result.get("issues", []))
                    total_issues += n
                    status = "OK" if n == 0 else f"{n}个问题"
                    print(f"  {os.path.basename(f)}: {status}")
            print(f"\n共检查 {len(sql_files)} 个文件，发现 {total_issues} 个问题")
        else:
            print(f"错误: {target} 不是有效的文件或目录")

    # --- procedure ---
    elif command == 'procedure':
        name = sys.argv[2] if len(sys.argv) > 2 else "my_procedure"
        # 解析参数: python dameng-tool.py procedure name p_date:DATE p_name:VARCHAR(100)
        params = []
        for arg in sys.argv[3:]:
            if ':' in arg:
                parts = arg.split(':', 1)
                params.append({"name": parts[0], "type": parts[1], "mode": "IN"})
            else:
                params.append({"name": arg, "type": "VARCHAR(100)", "mode": "IN"})
        template = tool.generate_procedure_template(name, params if params else None)
        print(template)

    # --- function ---
    elif command == 'function':
        name = sys.argv[2] if len(sys.argv) > 2 else "my_function"
        return_type = sys.argv[3] if len(sys.argv) > 3 else "VARCHAR(4000)"
        template = tool.generate_function_template(name, return_type)
        print(template)

    # --- trigger ---
    elif command == 'trigger':
        if len(sys.argv) < 4:
            print("错误: 请指定触发器名称和表名")
            print("用法: python dameng-tool.py trigger <名称> <表名> [类型]")
            print("类型: AFTER INSERT (默认) / AFTER UPDATE / BEFORE INSERT 等")
            return
        name = sys.argv[2]
        table = sys.argv[3]
        trig_type = sys.argv[4] if len(sys.argv) > 4 else "AFTER INSERT"
        template = tool.generate_trigger_template(name, table, trig_type)
        print(template)

    # --- test connect ---
    elif command == 'test':
        subcmd = sys.argv[2].lower() if len(sys.argv) > 2 else ''
        if subcmd != 'connect':
            print("错误: test子命令仅支持 connect")
            print("用法: python dameng-tool.py test connect [host] [port] [user] [password]")
            return
        host = sys.argv[3] if len(sys.argv) > 3 else 'localhost'
        port = int(sys.argv[4]) if len(sys.argv) > 4 else 5236
        user = sys.argv[5] if len(sys.argv) > 5 else ''
        password = sys.argv[6] if len(sys.argv) > 6 else ''
        result = tool.test_connect(host=host, port=port, user=user, password=password)
        print(tool.format_connect_result(result))
        if not result["connected"]:
            sys.exit(1)

    # --- sql format ---
    elif command == 'sql':
        subcmd = sys.argv[2].lower() if len(sys.argv) > 2 else ''
        if subcmd != 'format':
            print("错误: sql子命令仅支持 format")
            print("用法: python dameng-tool.py sql format <sql_file>")
            return
        if len(sys.argv) < 4:
            print("错误: 请指定SQL文件")
            return
        filepath = sys.argv[3]
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                sql = f.read()
            formatted = tool.format_sql(sql)
            print("格式化后的SQL:")
            print("-" * 60)
            print(formatted)
        except FileNotFoundError:
            print(f"错误: 文件不存在: {filepath}")
        except Exception as e:
            print(f"错误: {e}")

    # --- search ---
    elif command == 'search':
        if len(sys.argv) < 3:
            print("错误: 请指定搜索标签")
            print("用法: python dameng-tool.py search <tag1> [tag2] ...")
            return
        tags = sys.argv[2:]
        results = tool.search_by_tags(tags)
        print(tool.format_search_results(results))

    # --- 未知命令 ---
    else:
        print(f"未知命令: {command}")
        print("支持命令: analyze, optimize, convert, check, procedure, function, trigger, test, sql, search")


if __name__ == '__main__':
    main()
