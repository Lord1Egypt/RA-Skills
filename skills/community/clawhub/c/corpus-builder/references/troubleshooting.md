# 故障排除指南

## 常见问题

### 1. ChromaDB 错误

#### 问题：sqlite3 版本过低
```
RuntimeError: Your system has an unsupported version of sqlite3. 
Chroma requires sqlite3 >= 3.35.0.
```

**解决方案**:
```bash
# 方案 1: 安装 pysqlite3-binary（推荐）
pip3 install pysqlite3-binary --user

# 方案 2: 升级系统 sqlite3
sudo apt-get install sqlite3  # Ubuntu/Debian
sudo yum install sqlite3      # CentOS/RHEL

# 验证版本
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
```

#### 问题：Collection 不存在
```
chromadb.errors.NotFoundError: Collection [xxx] does not exist
```

**解决方案**:
```bash
# 检查语料库名称是否正确
python3 scripts/build_corpus.py --stats --collection 正确的名称

# 重新构建语料库
python3 scripts/build_corpus.py --source ~/novels --name 正确的名称
```

---

### 2. 内存过高

#### 问题：内存使用超过阈值
```
⚠️  警告：内存使用过高 (85.0%)
```

**解决方案**:
```bash
# 降低内存限制
python3 scripts/build_corpus.py \
    --source ./novels \
    --name test \
    --memory-limit 1500 \
    --batch-size 3

# 分批处理
python3 scripts/build_corpus.py \
    --source ./novels/part1 \
    --name test_part1

python3 scripts/build_corpus.py \
    --source ./novels/part2 \
    --name test_part2
```

---

### 3. LLM 调用失败

#### 问题：未配置 API Key
```
Exception: 未配置 DashScope API Key
```

**解决方案**:
```bash
# 设置环境变量
export DASHSCOPE_API_KEY="sk-xxx"

# 永久生效
echo 'export DASHSCOPE_API_KEY="sk-xxx"' >> ~/.bashrc
source ~/.bashrc

# 验证配置
echo $DASHSCOPE_API_KEY
```

#### 问题：API 调用超时
```
httpx.ReadTimeout: Request timed out
```

**解决方案**:
```bash
# 减小批量大小
python3 scripts/build_corpus.py \
    --source ./novels \
    --name test \
    --batch-size 2

# 使用规则降级模式（不设置 API Key）
# 系统会自动降级到规则标注
```

---

### 4. 向量化错误

#### 问题：模型加载失败
```
ModelLoadError: 模型加载失败
```

**解决方案**:
```bash
# 清理模型缓存
rm -rf ~/.cache/huggingface/hub/models--BAAI--bge-small-zh-v1.5

# 重新下载
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-zh-v1.5')"

# 检查网络连接
ping huggingface.co
```

#### 问题：向量维度不匹配
```
chromadb.errors.InvalidArgumentError: Collection expecting embedding with dimension of 512, got 384
```

**解决方案**:
```bash
# 删除语料库重新构建（使用正确的模型）
rm -rf corpus/chroma/xxx
python3 scripts/build_corpus.py --source ./novels --name xxx

# 检查模型配置
cat configs/default_config.yml | grep embedding
```

---

### 5. 文件处理错误

#### 问题：未找到 TXT 文件
```
❌ 错误：未找到 TXT 文件：/path/to/novels
```

**解决方案**:
```bash
# 检查目录是否存在
ls -la ~/workspace/novels/

# 检查文件扩展名
find ~/workspace/novels/ -name "*.txt"

# 转换编码（如果是 GBK 编码）
iconv -f GBK -t UTF-8 input.txt > output.txt
```

#### 问题：文件编码错误
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**解决方案**:
```bash
# 检测文件编码
file -i filename.txt

# 转换编码
iconv -f GBK -t UTF-8 filename.txt > filename_utf8.txt

# 或者使用 Python 转换
python3 -c "
import sys
with open('filename.txt', 'r', encoding='gbk') as f:
    content = f.read()
with open('filename_utf8.txt', 'w', encoding='utf-8') as f:
    f.write(content)
"
```

---

### 6. 断点续传

#### 问题：中途中断后恢复
```bash
# 使用 checkpoint 参数
python3 scripts/build_corpus.py \
    --source ./novels \
    --name test \
    --checkpoint corpus/cache/test_checkpoint.json

# 或者禁用缓存重新处理
python3 scripts/build_corpus.py \
    --source ./novels \
    --name test \
    --no-cache
```

---

## 调试技巧

### 1. 启用详细输出
```bash
python3 scripts/build_corpus.py --source ./novels --name test -v
```

### 2. 查看日志
```bash
# 查看最近的处理日志
tail -f /tmp/corpus-builder.log

# 查看错误日志
grep -i error /tmp/corpus-builder.log
```

### 3. 测试单个文件
```bash
# 创建测试目录
mkdir -p /tmp/test_corpus
cp ~/novels/第一章.txt /tmp/test_corpus/

# 处理单个文件
python3 scripts/build_corpus.py \
    --source /tmp/test_corpus \
    --name test_single \
    --batch-size 1
```

### 4. 检查依赖
```bash
# 验证 Python 版本
python3 --version  # 需要 >= 3.8

# 验证依赖安装
pip3 list | grep -E "chromadb|sentence-transformers|pyyaml"

# 重新安装依赖
cd ~/.openclaw/workspace/skills/corpus-builder
pip3 install -r requirements.txt --user
```

---

## 性能优化

### 1. 批量大小调整
```bash
# 大内存机器（16GB+）
--batch-size 10 --embedding_batch_size 64

# 中等内存（8GB）
--batch-size 5 --embedding_batch_size 32

# 小内存（4GB）
--batch-size 2 --embedding_batch_size 16
```

### 2. 并行处理
```bash
# 多进程处理（实验性）
python3 scripts/build_corpus.py \
    --source ./novels \
    --name test \
    --max_workers 4
```

### 3. 使用 SSD 存储
```bash
# 将语料库存储在 SSD 上
ln -s /mnt/ssd/corpus ~/.openclaw/workspace/skills/corpus-builder/corpus
```

---

## 获取帮助

### 1. 查看帮助
```bash
python3 scripts/build_corpus.py --help
```

### 2. 查看版本
```bash
cat ~/.openclaw/workspace/skills/corpus-builder/CHANGELOG.md
```

### 3. 报告问题
- GitHub Issues: https://github.com/openclaw/openclaw/issues
- 包含：错误信息、复现步骤、环境信息

---

*最后更新：2026-04-01*
