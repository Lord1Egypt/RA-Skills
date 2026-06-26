# 认知执行命令速查

## 脚本位置

所有脚本位于：`~/.workbuddy/skills/cogniexec/scripts/`

## 分类总览

| 类别 | 说明 | 脚本数 |
|------|------|--------|
| **A类** | LLM无法替代（系统API / 网络协议栈 / 二进制处理） | 11个 |
| **B类** | LLM能做但高频使用费token（效率替代型） | 6个 |

---

> **设计原则**：
> - **高频 + 标准化** → 预置脚本（省时间、省token）
> - **低频 / 一次性** → LLM按需动态生成（零维护成本）
>
> 缺失能力已有替代方案：专用技能插件（PDF→pdf技能、Excel→xlsx技能、PPT→pptx技能等）或第二层动态生成。无需补充新脚本。

# A类 — LLM无法替代（需系统API / 网络协议栈 / 二进制处理）

> 此类脚本执行的操作超出大语言模型的能力范围：需要调用操作系统API、建立网络连接、处理二进制文件、或进行确定性数学运算。**这是脚本存在的核心价值——使不可能变为可能。**

---

## A1 — 系统交互层（操作系统API）

### 1. clipboard.py - 剪贴板工具

#### 读取剪贴板
```
python clipboard.py read                    # 文本内容
python clipboard.py read-image -o clip.png  # 图片保存到文件
```

#### 写入剪贴板
```
python clipboard.py write "Hello World"     # 写入文本
python clipboard.py write-file report.txt   # 将文件内容写入剪贴板
python clipboard.py paste-image photo.png   # 将图片粘贴到剪贴板
```

#### 历史记录与检测
```
python clipboard.py history -n 10           # 最近10条历史
python clipboard.py detect                  # 检测剪贴板格式和编码
python clipboard.py clear                   # 清空剪贴板
```
依赖：纯标准库(Windows API)

---

### 2. tui_tool.py - 终端交互UI

#### 进度条
```
python tui_tool.py progress --total 100 --task "处理文件中..."
python tui_tool.py progress --total 500 --task "下载中..." --unit MB
```

#### 加载动画
```
python tui_tool.py spinner --text "加载资源..." --style dots
python tui_tool.py spinner --text "处理中..." --style arrows
```
样式选项：`dots`, `arrows`, `bars`, `snake`

#### 选择列表
```
python tui_tool.py select --options "选项A","选项B","选项C" --prompt "请选择:"
python tui_tool.py select --options a,b,c,d,e,f --multi --search   # 多选+搜索过滤
```

#### 其他交互组件
```
python tui_tool.py confirm --prompt "确认删除吗？"
python tui_tool.py table --data '[{"name":"Alice","age":25},{"name":"Bob","age":30}]'
python tui_tool.py input --prompt "请输入用户名:" --required
python tui_tool.py input --prompt "请输入密码:" --password
python tui_tool.py input --prompt "请输入年龄:" --type int --min 1 --max 150
python tui_tool.py countdown --seconds 30 --message "操作将在...后自动继续"
```
依赖：纯标准库

---

## A2 — 网络通信层（TCP/IP协议栈）

### 3. http_client.py - HTTP客户端

#### GET / POST 请求
```
python http_client.py get https://api.example.com/users --header "Authorization: Bearer xxx"
python http_client.py post https://httpbin.org/post --data '{"test":1}' --json
python http_client.py head https://api.example.com/health              # 查看头信息
```

#### 下载与断链检测
```
python http_client.py download https://example.com/file.zip -o file.zip
python http_client.py check-urls urls.txt -o report.json --concurrent 5
```

#### 高级功能
```
python http_client.py api-swagger https://petstore.swagger.io/v2/swagger.json
python http_client.py debug-request https://api.example.com/data get
```
依赖：纯标准库(urllib)

---

### 4. net_diag.py - 网络诊断工具

#### Ping 检测
```
python net_diag.py ping example.com -c 4
python net_diag.py ping github.com -c 10 --timeout 3
```

#### DNS 解析
```
python net_diag.py dns example.com --type A
python net_diag.py dns example.com --type A,MX,TXT,NS
python net_diag.py resolve github.com                     # 完整解析
```

#### 端口探测
```
python net_diag.py port example.com 80,443,8080
python net_diag.py port example.com 1-1024 --timeout 1
```

#### 路由追踪与健康检查
```
python net_diag.py traceroute example.com --max-hops 20
python net_diag.py http-check https://api.example.com/health --expected 200
```

#### 信息查询
```
python net_diag.py ip-info 8.8.8.8
python net_diag.py speed-test
```
依赖：纯标准库(socket)

---

### 5. email_sender.py - 邮件发送

#### 发送邮件（通过环境变量 SMTP_HOST/SMTP_USER/SMTP_PASSWORD 配置）
```
python email_sender.py send --to "user@example.com" --subject "测试" --body "Hello"
```

#### HTML邮件 + 附件 + 抄送密送
```
python email_sender.py send --to "a@x.com,b@x.com" --cc "cc@x.com" \
    --subject "月报" --html --body "<h1>Hi</h1>" --attach report.pdf
```

#### 批量与测试
```
python email_sender.py send --template emails.jsonl --data users.json --dry-run
python email_sender.py test-connection --host smtp.gmail.com --port 587 --tls
python email_sender.py preview --body "<h1>Title</h1>" -o preview.html
python email_sender.py validate contacts.txt
```
依赖：纯标准库(smtplib)

---

## A3 — 数据存储层（结构化存储引擎）

### 6. db_tool.py - SQLite数据库工具

#### 创建数据库和表
```
python db_tool.py create mydb.sql --table users --columns id:INTEGER:PK,name:TEXT,email:TEXT,age:INTEGER
```

#### SQL 查询与执行
```
python db_tool.py query mydb.sql "SELECT * FROM users WHERE age > 25"
python db_tool.py query mydb.sql "INSERT INTO users(name,email) VALUES('张三','zhang@example.com')"
python db_tool.py exec mydb.sql "UPDATE users SET age=30 WHERE id=1"
```

#### CSV ↔ 数据库互转
```
python db_tool.py import-csv data.csv --db output.db --table records
python db_tool.py export-csv mydb.sql --table users -o backup.csv --encoding utf-8-sig
```

#### Schema 与管理
```
python db_tool.py schema mydb.sql --table users --detail
python db_tool.py index mydb.sql --table orders --add --column user_id --name idx_user
python db_tool.py batch mydb.sql migrations/sql
python db_tool.py stats mydb.sql
```
依赖：纯标准库(sqlite3)

---

### 7. git_advanced.py - Git高级操作

#### Stash 暂存
```
python git_advanced.py stash save "临时保存工作进度"
python git_advanced.py stash list
python git_advanced.py stash pop
python git_advanced.py stash drop 0          # 丢弃指定stash
python git_advanced.py stash clear           # 清除所有
```

#### Blame 逐行修改历史
```
python git_advanced.py blame src/main.py
python git_advanced.py blame src/utils.py -s 10 -e 30    # 指定行范围
```

#### Diff 差异对比
```
python git_advanced.py diff HEAD~5 HEAD --stat
python git_advanced.py diff main..feature --name-only
python git_advanced.py diff --cached                        # 暂存区 vs HEAD
```

#### Cherry-pick / Rebase / 冲突解决
```
python git_advanced.py cherry-pick abc1234 def5678
python git_advanced.py rebase info                           # 查看变基前状态
python git_advanced.py rebase start main                     # 开始变基到 main
python git_advanced.py rebase continue                       # 继续变基
python git_advanced.py rebase abort                          # 中止变基
python git_advanced.py conflicts list                        # 列出冲突文件
python git_advanced.py conflicts ours src/file.py            # 采用 ours 版本
python git_advanced.py conflicts theirs src/file.py          # 采用 theirs 版本
```

#### 图形化日志与 Hooks 管理
```
python git_advanced.py log-graph -n 20 --author "张三"
python git_advanced.py hooks list                             # 列出所有 hooks 状态
python git_advanced.py hooks enable pre-commit
python git_advanced.py hooks disable pre-push
```
依赖：纯标准库(subprocess+git)

---

### 8. archive_tool.py - 压缩归档工具

#### ZIP 操作
```
python archive_tool.py zip ./project -o project.zip
python archive_tool.py unzip project.zip -o ./extracted
python archive_tool.py zip ./secret -o secret.zip --password "mypwd"
python archive_tool.py zip huge_folder/ -o backup.zip --volume-size 500MB    # 多卷分拆
```

#### TAR.GZ / TAR / GZ
```
python archive_tool.py tar-gz ./logs -o logs.tar.gz
python archive_tool.py untar logs.tar.gz -o ./extracted_logs
python archive_tool.py gzip largefile.txt
python archive_tool.py gunzip largefile.txt.gz
```

#### 归档信息与校验
```
python archive_tool.py info project.zip --list-files         # 列出内嵌文件详情
python archive_tool.py verify backup.zip                      # 校验完整性
```
依赖：纯标准库(zipfile/tarfile/gzip)

---

## A4 — 二进制处理层（精确字节运算）

### 9. crypto_utils.py - 加密与精确计算

#### 哈希计算（多算法）
```
python crypto_utils.py hash file.txt --algo sha256
python crypto_utils.py hash "Hello World" --text --algo md5 --all     # 输出所有常用算法
```
支持算法：md5, sha1, sha224, sha256, sha384, sha512, blake2b, blake2s

#### 安全密码生成
```
python crypto_utils.py password --length 32 --special --no_ambiguous -n 5
python crypto_utils.py password --length 16 --alpha-numeric             # 仅字母数字
```

#### UUID / HMAC / Base64 / XOR
```
python crypto_utils.py uuid -n 5 --no-dash                              # 无横线UUID
python crypto_utils.py hmac secret-key "message to sign"
python crypto_utils.py base64-encode "Hello World" --url-safe
python crypto_utils.py xor-crypt "secret message" "key123"
```

#### 校验和 / 令牌 / 文件对比
```
python crypto_utils.py checksum file.bin --compare "md5:abc123"
python crypto_utils.py token --bytes 32 --format urlsafe -n 3
python crypto_utils.py compare-files a.bin b.bin
```
依赖：纯标准库(hashlib/hmac/secrets/base64)

---

### 10. image_batch.py - 图像批处理

#### 图像信息查看
```
python image_batch.py info photo.jpg
python image_batch.py info ./photos/
```

#### 批量缩放 / 压缩 / 水印
```
python image_batch.py batch-resize ./photos -w 1920 -h 1080 -o ./resized
python image_batch.py compress ./images --quality 70
python image_batch.py watermark ./photos --text "©2025" --position bottom-right
python image_batch.py watermark ./photos --image logo.png --position top-left --opacity 0.7
```

#### 格式转换 / 裁剪 / 旋转
```
python image_batch.py convert ./images png jpg -o ./converted
python image_batch.py crop ./photos --left 100 --top 50 --width 800 --height 600
python image_batch.py rotate ./photos --angle 90
python image_batch.py rotate ./photos --auto                # EXIF方向自动校正
```

#### 缩略图 / 拼贴画
```
python image_batch.py thumbnail ./photos --size 256 -o ./thumbs
python image_batch.py grid ./photos --cols 4 -o collage.png
python image_batch.py grid ./photos --rows 3 --gap 10 --border 2 -o collage.png
```
依赖：标准库+pillow(可选)

---

### 11. qr_tool.py - 二维码生成与解析

#### 生成二维码
```
python qr_tool.py generate "https://example.com" -o qrcode.png
python qr_tool.py generate "Hello 世界" --size 20 --fill-color "#FF5733" --bg-color "#FFFFFF"
python qr_tool.py generate "WiFi密码是abc123" --error-correction H      # 高容错级别
```

#### 解码二维码图片
```
python qr_tool.py decode qrcode.png
python qr_tool.py decode ./qr_codes/
```

#### WiFi 配置二维码（手机扫描自动连接）
```
python qr_tool.py wifi "MyNetwork" "password123" -o wifi.png
python qr_tool.py wifi "MyNetwork" "pwd123" --security WPA -o wifi.png
```

#### vCard 联系人 / 批量生成
```
python qr_tool.py vcard "张三" "13800138000" "zhangsan@example.com" --org "ABC公司" -o card.png
python qr_tool.py batch urls.txt -o output/
```
支持协议：`WPA`, `WEP`, `nopass`
依赖：标准库+qrcode(可选)，解码需pyzbar

---

# B类 — LLM能做但高频使用费token（效率替代型）

> 此类脚本的 task 大语言模型原生能力可覆盖（本质是文本处理），但在高频场景下用脚本更省token、更快、结果更确定。**核心价值——节省推理成本、突破上下文窗口限制、保证输出一致性。**

---

## B1 — 格式转换

### 12. format_converter.py - 格式转换工具

#### 数据格式互转
```
python format_converter.py json2yaml config.json -o config.yaml
python format_converter.py yaml2json config.yaml
python format_converter.py json2toml data.json
python format_converter.py toml2json config.toml
python format_converter.py ini2json settings.ini
python format_converter.py json2ini data.json -o settings.ini
python format_converter.py csv2json data.csv --encoding utf-8-sig
python format_converter.py json2csv data.csv -o output.csv
python format_converter.py json2env settings.json -o .env
python format_converter.py env2json .env
```

#### 日期时间处理
```
python format_converter.py date-format "2024-01-15" --to-fmt "%Y年%m月%d日"
python format_converter.py timestamp                      # 当前时间戳
python format_converter.py timestamp 1705276800            # 时间戳→日期
python format_converter.py duration-calc "2h30m" --to-minutes
```

#### 环境文件 / JSON美化
```
python format_converter.py generate-env .env.example -o .env
python format_converter.py json-pretty data.json
python format_converter.py json-pretty data.json --compress
```
注：Base64/URL编解码 → crypto_utils.py；Markdown→HTML → text_utils.py
依赖：纯标准库

---

## B2 — 数据处理

### 13. data_processor.py - 数据处理引擎

#### 过滤与排序
```
python data_processor.py filter data.csv --where "age>30" -o filtered.csv
python data_processor.py sort data.csv --by salary --desc
python data_processor.py head-tail data.csv -n 10               # 前10行
python data_processor.py tail data.csv -n 5                     # 后5行
```

#### 分组聚合与统计
```
python data_processor.py group data.csv --by dept --agg avg:salary,count:id,sum:bonus
python data_processor.py stats data.csv --columns price,quantity
python data_processor.py stack files*.csv -o combined.csv        # 纵向合并
```

#### 透视表 / 变换
```
python data_processor.py pivot data.csv --rows dept --cols month --values sales
python data_processor.py transform data.csv --map "total=price*qty" -o result.csv
python data_processor.py fill data.csv --column age --strategy mean   # 缺失值填充
```

#### 去重 / 合并 / 采样
```
python data_processor.py dedup data.csv --by email -o clean.csv
python data_processor.py merge users.csv orders.csv --on user_id -o joined.csv
python data_processor.py sample data.csv --n 100 --random
python data_processor.py info data.csv                               # 数据集概览
```
策略选项：mean, median, mode, constant, forward-fill, backward-fill, drop
依赖：纯标准库

---

## B3 — JSON查询

### 14. jq_tool.py - JSONPath查询器

#### 路径提取
```
python jq_tool.py get data.json "$.users[0].name"
python jq_tool.py get data.json "$.items[*].price"
python jq_tool.py get data.json "$.users[*].address.city"           # 嵌套提取
```

#### 过滤与变换
```
python jq_tool.py filter data.json "$.users[*]" --where "age>30" -o adults.json
python jq_tool.py map data.json "$.items[*]" --expr "price*1.1" -o taxed.json
python jq_tool.py flatten data.json "$.users[*].orders"              # 展开嵌套数组
```

#### 格式化输出
```
python jq_tool.py format data.json --pretty
python jq_tool.py format data.json --output-format csv
python jq_tool.py format data.json --output-format table
```

#### 键值操作与比较
```
python jq_tool.py keys data.json "$.users[0]"                       # 列出所有键
python jq_tool.py merge file1.json file2.json -o merged.json
python jq_tool.py sort data.json "$.users[*]" --by age
python jq_tool.py validate data.json                                 # JSON合法性检查
python jq_tool.py diff old.json new.json                             # 差异比较
python jq_tool.py from-yaml config.yaml -o config.json               # YAML→JSON
```
依赖：纯标准库(json)

---

## B4 — 文本处理

### 15. text_utils.py - 文本处理工具

#### Diff 对比
```
python text_utils.py diff file_a.txt file_b.txt
python text_utils.py diff "Hello World" "Hello Python" --text --format stats
```

#### 正则提取与替换
```
python text_utils.py regex-extract data.txt --pattern "\d+\.\d+"
python text_utils.py regex-replace input.txt --pattern "\\b\\w+\\b" --replacement "[MATCH]"
```
标志支持：i(忽略大小写), m(多行), s(点匹配换行)

#### 文本统计分析
```
python text_utils.py stats article.md --words --chars --lines --sentences
python text_utils.py word-frequency essay.txt --top 30
```

#### 编码与模板
```
python text_utils.py encode-detect messy.txt                         # 自动检测编码
python text_utils.py convert-encoding file.txt --from gb2312 --to utf-8
python text_utils.py fill-template template.jsonl data.json
```

#### 提取与清理
```
python text_utils.py extract-emails contacts.txt
python text_utils.py extract-urls page.html
python text_utils.py wrap-text long_text.txt --width 80
python text_utils.py trim-whitespace messy.txt
```

#### Markdown → HTML
```
python text_utils.py md2html readme.md -o readme.html
python text_utils.py md2html doc.md -o doc.html --css style.css
```
依赖：纯标准库

---

## B5 — 文件批量操作

### 16. file_manager.py - 文件批量操作

#### 文件归类
```
python file_manager.py classify ./Downloads --by ext -o ./Sorted       # 按扩展名
python file_manager.py classify ./folder --by size --threshold 10MB    # 按大小
```

#### 批量重命名
```
python file_manager.py rename ./photos --pattern "IMG_{seq:04d}.jpg"
python file_manager.py rename ./files --pattern "{name}_backup{ext}"
```

#### 文件去重
```
python file_manager.py dedup ./folder --by content --dry-run
python file_manager.py dedup ./folder --by name
python file_manager.py dedup ./folder --by size
```

#### 目录扫描与搜索
```
python file_manager.py scan ./project --size-sort --top 20 -o report.json
python file_manager.py find ./src --name "*.py" --contains "TODO" --depth 3
```

#### 清理 / 树形展示 / 同步
```
python file_manager.py clean ./folder --older-than 30d --pattern "*.tmp" --dry-run
python file_manager.py tree ./project --depth 3 --size
python file_manager.py sync ./src ./backup --dry-run
python file_manager.py archive ./logs --zip --older-than 7d
```

#### 批量文本替换
```
python file_manager.py batch-replace ./src --from "old_api" --to "new_api" --ext .py
```
依赖：纯标准库

---

## B6 — 代码工具

### 17. code_tools.py - 代码工具集

#### 语法校验
```
python code_tools.py lint ./src --ext .py,.js,.ts
python code_tools.py lint single_file.py                            # 单文件检查
```
支持语言：Python, JavaScript, TypeScript, JSON, HTML, CSS

#### TODO/FIXME 扫描
```
python code_tools.py find-todo ./src --tags TODO,FIXME,HACK,XXX
python code_tools.py find-todo ./src --tags TODO,FIXME --format json -o todos.json
```

#### API 提取
```
python code_tools.py extract-api app.py --framework flask
python code_tools.py extract-api server.py --framework fastapi
```
支持框架：Flask, FastAPI, Django, Express

#### 统计与 Git 辅助
```
python code_tools.py count-lines ./project --by ext
python code_tools.py git-log -n 10 --format short
python code_tools.py git-branch --all
```

#### 代码搜索与语言检测
```
python code_tools.py search-code "def.*process" ./src --ext .py
python code_tools.py detect-lang unknown_file
python code_tools.py check-imports ./src --missing-only
```
依赖：纯标准库


---
