---
name: eternal-memory
description: "五层记忆系统：本地向量引擎+追加不修改归档+L1c三重校验+拓扑评分+冷热分离。永不失忆，自愈降级。零云依赖。"
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      packages: ["numpy"]
    optional:
      - fastembed  # ONNX加速（可选）
homepage: https://github.com/yy885/eternal-memory
license: MIT
tags: [memory, vector, archive, verification, self-healing, offline-first]
price: 0
---

# Eternal Memory — 永不失忆的五层记忆系统

> 本地向量引擎 + 追加不修改归档 + L1c三重校验 = 零云依赖的不可变记忆。

**5.9ms延迟 · 741文件SHA256锚定 · 500/500校验通过 · 零网络**

## 触发词

记忆系统 向量引擎 归档 冷热分离 记忆校验 永不失忆 L1c 五层记忆 eternal memory

---

## 一、为什么选Eternal Memory？

| 对手 | 他们有 | 我们也有 | 我们有，他们没有 |
|------|--------|----------|-----------------|
| Mem0 | 云端向量 | 本地TF-IDF | **L1c三重校验** |
| GraphRAG | 知识图谱 | 知识图谱 | **追加不修改+拓扑评分** |
| engram | FTS5 | FTS5 | **冷热分离+降级自愈** |
| TencentDB | 符号压缩 | 符号压缩 | **离线可用+校验链** |

**独有壁垒：L1c校验（哈希+语义+拓扑）— 行业唯一。检索结果自动验证，校验失败自动降级到全原始加载。**

---

## 二、安装

```bash
# 1. 通过ClawHub安装
clawhub install eternal-memory

# 2. 手动安装
cp -r eternal-memory/tools/* ~/.openclaw/workspace/tools/

# 3. 初始化
python3 tools/memory_system.py --archive

# 4. 验证
python3 tools/memory_topology.py --benchmark 50
# 期望: 成功50/50 | 校验250✅/0⚠️ | 延迟avg<10ms
```

零外部依赖（Python 3.8+ + numpy），任何环境都能跑。ONNX可选加速（pip install fastembed）。

---

## 三、架构总览

```
L5 应用层 ─── 对话/交易/代码 三模态
L4 存储层 ─── 🔥热(SSD) 🌤️温 ❄️冷(gzip)
L3 技能层 ─── 进化工坊/经验库
L2 索引层 ─── FTS5 + 图谱 + 拓扑(5因子)
L1 归档层 ─── L1a(SHA256) → L1b_pre(压缩) → L1b(RRF+MMR) → L1c(校验★)
```

### L1c 三重校验（核心壁垒）

```
检索结果 → ①哈希校验(SHA256锚定)
            ├─ 未通过 → 报警+降级
            └─ 通过 → ②语义校验(向量/Jaccard/字面)
                      ├─ 未通过 → 降级到全原始
                      └─ 通过 → ③拓扑校验(引用链完整)
                                └─ 返回可信结果
```

### 降级自愈链

```
FTS5+向量+图谱 →(损坏)→ 图谱降级 →(损坏)→ 归档搜索 →(损坏)→ rebuild-index 恢复
```

---

## 四、核心工具

| 工具 | 功能 | 命令示例 |
|------|------|---------|
| `local_embedder.py` | 本地向量引擎(TF-IDF/ONNX三层) | `SKIP_ONNX=1 python3 tools/local_embedder.py` |
| `unified_search_ng.py` | 搜索引擎(RRF+MMR+L1c) | `python3 tools/unified_search_ng.py "记忆系统" --verbose` |
| `memory_topology.py` | 拓扑评分+冷热分离+降级演练 | `python3 tools/memory_topology.py --score --migrate --benchmark` |
| `symbolic_compressor.py` | 符号压缩(5模板+Mermaid) | `python3 tools/symbolic_compressor.py --compress memory/` |
| `memory_system.py` | 系统编排(守护+校验+重建) | `python3 tools/memory_system.py --wake --verify-integrity` |

---

## 五、性能基准

```
延迟: avg 5.9ms  p50 6ms  p99 8ms  (100轮)
校验: 500/500 ✅  零降级
归档: 741文件 SHA256 100%锚定
拓扑: 139节点 热10/温96/冷33
降级: 4阶段链 全部通过
```

---

## 六、守护进程配置

```bash
# 添加到crontab（每5分钟增量扫描）
*/5 * * * * cd ~/.openclaw/workspace-v4-pro && python3 tools/memory_system.py --wake

# 每天一次拓扑评分
0 3 * * * cd ~/.openclaw/workspace-v4-pro && python3 tools/memory_topology.py --score
```

---

## 💛 赞助支持

如果Eternal Memory帮你省了Mem0的API费用，或让你的Agent真正"永不失忆"——

- **微信/支付宝** 扫码赞助（见 assets/wechat_pay.jpg / assets/alipay.jpg）
- **GitHub Sponsor** 即将开通
- **企业支持** $299/次 定制集成 · 联系见GitHub

---

## 兼容性

- Python 3.8+ | macOS / Linux / WSL2
- 零网络依赖（Tier 2 TF-IDF模式）
- ONNX可选增强（pip install fastembed）
