# 📝 模块 2：文本工具

---

#### 2.1 文本统计

**✅ 开箱即用**

<details>
<summary>📋 展开查看命令</summary>

```python
t = input("输入文本:")
if not t or not t.strip():
    print("❌ 没有检测到输入。请程序运行时输入一段文字")
else:
    total = len(t)
    cn = sum(1 for c in t if '一' <= c <= '鿿')
    en = len(t.split())
    lines = t.split(chr(10))
    print(f"总字符: {total} | 中文: {cn} | 英文词: {en}")
    print(f"非空行: {len([l for l in lines if l.strip()])}")
    print(f"去重后: {len(list(dict.fromkeys(lines)))}行 (原{len(lines)}行)")
```

</details>

---

#### 2.2 编码转换 ⭐ v3.9.0 拆分为 encode + hash

> v3.9.0 将编码转换拆分为两个独立工具：`text.encode`（Base64/URL/Unicode/进制）和 `text.hash`（MD5/SHA1/SHA256）。

<details>
<summary>📋 text.encode（Base64/URL/Unicode/进制）</summary>

```python
import base64, urllib.parse
try:
    t = input("文本:") or "Hello"
    m = input("方法(Base64/URL/Unicode/进制):").strip() or "Base64"
    op = input("编码/解码:").strip() or "编码"
    if m == "Base64":
        print(base64.b64encode(t.encode()).decode() if op == "编码" else base64.b64decode(t.encode()).decode())
    elif m == "URL":
        print(urllib.parse.quote(t) if op == "编码" else urllib.parse.unquote(t))
    elif m == "Unicode":
        print(" ".join(f"\\u{ord(c):04x}" for c in t))
    elif m == "进制":
        base_from = input("原进制(2/8/10/16):").strip() or "10"
        try:
            n = int(t, int(base_from))
            print(f"✅ {t} (原{base_from}进制) =")
            print(f"   二进制: {bin(n)[2:]}")
            print(f"   八进制: {oct(n)[2:]}")
            print(f"   十进制: {n}")
            print(f"   十六进制: {hex(n)[2:].upper()}")
        except ValueError:
            print(f"❌ '{t}' 不是有效的{base_from}进制数字")
    else:
        print(f"❌ 不支持 {m}。可选: Base64 / URL / Unicode / 进制")
except Exception as e:
    print(f"❌ 处理失败: {e}")
```

</details>

<details>
<summary>📋 text.hash（MD5/SHA1/SHA256）</summary>

```python
import hashlib
try:
    t = input("文本:") or "Hello"
    algos = {"md5": hashlib.md5(), "sha1": hashlib.sha1(), "sha256": hashlib.sha256()}
    for name, h in algos.items():
        h.update(t.encode())
        print(f"  {name.upper():7}: {h.hexdigest()}")
except Exception as e:
    print(f"❌ {e}")
```

</details>

---

#### 2.3 词频统计

**✅ 开箱即用**

<details>
<summary>📋 展开查看命令</summary>

```python
from collections import Counter
import re

STOPWORDS = {'的','了','和','是','在','我','有','也','不','就','都','而','及','与','着','或','一个','没有',
    '我们','你们','他们','她们','但是','然而','因为','所以','如果','虽然','不过','而且','或者','还是',
    '既','又','并','等','把','被','让','往','从','对','于','以','为','比','此','那','这','她','他','它',
    '们','些','什么','哪','怎么','多','很','最','更','太','非常','每','当','起','已','将','能','会','应',
    '可','得','过','给','来','去','说','看','知道','做','想','问','请','好','再','还','只','如','真的',
    '自己','人','事','时','地','今天','现在','一些','这样','那样','怎么样','可以','这个','那个','不是',
    '可能','已经','之后','之前','然后','不过','比较','其实','其他','其中','所有','虽然','由于','因此'}

def _smart_segment(text):
    try:
        import jieba
        return list(jieba.lcut(text, cut_all=False))
    except ImportError:
        return re.findall(r'[一-鿿\w]+', text)

try:
    t = input("输入文本:")
    if not t.strip():
        print("❌ 没有检测到输入")
    else:
        raw = _smart_segment(t)
        words = []
        for w in raw:
            w = w.strip()
            if len(w) <= 1: continue
            if re.match(r'^[a-zA-Z]+$', w): w = w.lower()
            if w in STOPWORDS: continue
            words.append(w)
        if not words:
            print("❌ 没有找到有效词")
        else:
            for i,(word,cnt) in enumerate(Counter(words).most_common(15),1):
                print(f"  {i:2d}. {word}: {cnt} {'█'*min(cnt*2,30)}")
            unique = len(set(words))
            print(f"\n📊 共 {len(words)} 个有效词，{unique} 个不重复词")
            d = unique/len(words)*100
            print(f"   词汇丰富度: {d:.1f}%", end="")
            print("（用词多样）" if d>80 else "（正常范围）" if d>50 else "（同词重复较多）")
            try:
                import jieba; print("   ✅ 已使用 jieba 精准分词")
            except: print("   💡 安装 jieba 可获得更精准分词: pip install jieba")
except Exception as e:
    print(f"❌ {e}")
```

</details>

---

#### 2.4 文本差异对比 ⭐ v3.7.0 新增

**✅ 开箱即用**（纯 Python 标准库 difflib，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import difflib, os

def _read(src):
    """支持文件路径或直接文本"""
    if os.path.isfile(src):
        with open(src, encoding="utf-8") as f:
            return f.read().splitlines()
    return src.split("\n")

src_a = input("文本A(内容或文件路径):").strip()
src_b = input("文本B(内容或文件路径):").strip()
if not src_a or not src_b:
    print("❌ 文本A和B均不能为空")
else:
    lines_a = _read(src_a)
    lines_b = _read(src_b)
    diff = list(difflib.unified_diff(lines_a, lines_b, lineterm="", fromfile="A", tofile="B"))
    if not diff:
        print("✅ 两段文本完全相同，无差异")
    else:
        for line in diff:
            if line.startswith("-") and not line.startswith("---"):
                print(f"🔴 {line}")
            elif line.startswith("+") and not line.startswith("+++"):
                print(f"🟢 {line}")
            elif line.startswith("@@"):
                print(f"🔵 {line}")
            else:
                print(f"   {line}")
        adds = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
        dels = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
        print(f"\n📊 新增 {adds} 行，删除 {dels} 行")
```

</details>
