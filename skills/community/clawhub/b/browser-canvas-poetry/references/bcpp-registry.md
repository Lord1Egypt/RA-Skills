# BCPP Registry - 去中心化艺术协议注册表

> 让BCPP成为真正的开放协议，而非单一组织的产品

---

## 核心理念

BCPP Registry 是一个**去中心化的开放系统**，类似于W3C标准、OpenGL规范，但服务于浏览器原生艺术。

任何人都可以：
- 创建新的渲染引擎
- 定义新的元素类型
- 发布艺术作品
- 注册新的流派

**没有人拥有BCPP，但每个人都是BCPP的一部分。**

---

## Registry 结构

### 1. 渲染器注册表 (Renderer Registry)

```yaml
# 渲染器注册条目
registry:
  type: "renderer"
  id: "bcpp-renderer-particleflow"
  name: "ParticleFlow Renderer"
  version: "1.0.0"

  # 谁创建的
  creator:
    name: "Canvas Poetry Collective"
    key: "bcpp1...xyz789"  # Base58公钥

  # 技术规格
  spec:
    platform: "web"
    engine: "webgl"
    capabilities:
      - "particle_system"
      - "fluid_simulation"
      - "glow_effects"
    performance:
      target_fps: 60
      max_particles: 10000

  # 接口契约
  interface:
    input: "BCPP-Elements"
    output: "WebGL-Render"
    config_schema: "https://registry.bcpp.art/schemas/renderer-config"

  # 验证签名
  signature:
    algorithm: "ed25519"
    key: "bcpp1...creator_key"
    timestamp: "2024-01-15T10:00:00Z"
```

### 2. 元素类型注册表 (Element Registry)

```yaml
# 元素类型注册条目
registry:
  type: "element"
  id: "bcpp-element-fluid"
  name: "Fluid Surface"
  version: "1.0.0"

  creator:
    name: "Fluid Art Lab"
    key: "bcpp1...fluid_lab"

  spec:
    category: "surface"
    properties:
      - name: "viscosity"
        type: "float"
        range: [0.0, 1.0]
        default: 0.5
      - name: "color"
        type: "color"
        default: "#1a3a5a"
      - name: "distortion"
        type: "float"
        range: [0.0, 2.0]

    behaviors:
      - "wave_propagation"
      - "interaction_response"
      - "reflection"

  renderer_support:
    - renderer_id: "bcpp-renderer-particleflow"
      compatibility: "full"
    - renderer_id: "bcpp-renderer-canvas2d"
      compatibility: "partial"
      limitations: ["reduced particle count"]
```

### 3. 流派注册表 (Genre Registry)

```yaml
# 流派注册条目
registry:
  type: "genre"
  id: "bcpp-genre-aurora"
  name: "极光派"
  name_en: "Aurora School"

  creator:
    name: "Aurora Collective"
    key: "bcpp1...aurora"

  spec:
    description: |
      以极光般的渐变和光晕为核心表现手段的艺术流派。
      强调色彩的流动性和光的神秘感。

    aesthetics:
      - "渐变至上"
      - "光晕渲染"
      - "色彩流动"
      - "夜空意象"

    color_palette:
      primary:
        - "#00ff87"
        - "#60efff"
        - "#ff61f6"
      secondary:
        - "#1a1a2e"
        - "#0a0a1a"

    constraints:
      motion:
        type: "flowing"
        speed: "slow"
      interaction:
        preferred: "mouse_move"

    examples:
      - "manifest_id: bcpp-art-001"
      - "manifest_id: bcpp-art-042"

  version: "1.0.0"
```

### 4. 作品注册表 (Artwork Registry)

```yaml
# 艺术作品注册条目
registry:
  type: "artwork"
  id: "bcpp-art-001"
  title: "落霞与孤鹜"

  creator:
    name: "AI Orchestrator"
    key: "bcpp1...ai_gen"

  spec:
    genre: "bcpp-genre-shuimohua"
    duration: 30000
    complexity: "medium"

    intention_summary:
      concept: "自然与人文的和谐共生"
      mood: ["壮丽", "孤独", "宁静"]

    technical:
      elements_count: 8
      renderers_used: ["bcpp-renderer-particleflow"]
      dependencies:
        - "bcpp-element-gradient"
        - "bcpp-element-particle"

  signature:
    algorithm: "ed25519"
    digest: "sha256_of_manifest"
    creator_key: "bcpp1...creator"
    timestamp: "2024-01-15T10:30:00Z"

  # 作品哈希（用于去重和引用）
  content_hash: "Qm...artwork_hash"
```

---

## 注册流程

### 注册新的渲染器

```bash
# 1. 准备渲染器定义文件
cat > my-renderer.yaml << EOF
registry:
  type: "renderer"
  id: "my-custom-renderer"
  name: "My Renderer"
  # ... 完整定义
EOF

# 2. 用私钥签名
bcpp-cli sign my-renderer.yaml --key my-private-key.pem

# 3. 提交到Registry
bcpp-cli register my-renderer.yaml.signed

# 4. 等待验证（可选，由社区投票）
```

### 发现和使用注册的渲染器

```bash
# 搜索渲染器
bcpp-cli search --type renderer --platform web --capability particle_system

# 结果
# - bcpp-renderer-particleflow v1.0.0
# - bcpp-renderer-fluidsim v2.1.0

# 查看渲染器详情
bcpp-cli info bcpp-renderer-particleflow

# 在manifest中使用
# render:
#   engine: "bcpp-renderer-particleflow"
```

---

## 治理机制

### 社区治理

```
┌─────────────────────────────────────────────────────────────┐
│                    BCPP Registry 治理                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  提案阶段                                                    │
│    ↓                                                        │
│  技术委员会评审 (5人)                                         │
│    ↓ 批准/拒绝                                              │
│  社区投票 (Simple Majority)                                  │
│    ↓ 超过50%同意                                            │
│  注册到Registry                                             │
│    ↓                                                        │
│  社区使用和反馈                                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 争议解决

```yaml
dispute_resolution:
  process:
    - step: 1
      action: "direct_negotiation"
      timeout: "7 days"
    - step: 2
      action: "mediation"
      mediator: "BCPP Council"
      timeout: "14 days"
    - step: 3
      action: "arbitration"
      arbitrator: "community_vote"
```

---

## 技术实现

### 去中心化存储

```
┌─────────────────────────────────────────────────────────────┐
│                    BCPP Registry 存储                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  IPFS / Filecoin          备份层 (作品、渲染器定义)           │
│       ↓                                                         │
│  内容寻址                                                      │
│       ↓                                                         │
│  ENS / DNSLink              解析层 (指向IPFS哈希)             │
│       ↓                                                         │
│  HTTPS (可选)              便捷层 (前端、SDK)                  │
│                                                              │
│  LocalStorage (可选)        缓存层 (离线使用)                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 签名验证

```typescript
// 验证注册条目签名
async function verifyRegistryEntry(entry: RegistryEntry): Promise<boolean> {
  // 1. 提取签名和公钥
  const { signature, creator } = entry.signature;

  // 2. 从Creator Key解析公钥
  const publicKey = await resolvePublicKey(creator.key);

  // 3. 计算内容的哈希
  const contentHash = sha256(JSON.stringify(entry.spec));

  // 4. 验证签名
  return verifyEd25519({
    message: contentHash,
    signature: signature,
    publicKey: publicKey
  });
}

// 防伪冒
async function checkKeyRevocation(key: string): Promise<boolean> {
  const revocationList = await fetch('ipfs://bcpp-revocation-list');
  return revocationList.includes(key);
}
```

---

## 激励设计

### 贡献者激励

```yaml
incentives:
  renderer_developer:
    reward: "registry_badge"
    criteria: "3+ renderers registered, 100+ uses"

  genre_creator:
    reward: "featured_listing"
    criteria: "genre used in 10+ artworks"

  artwork_creator:
    reward: "creator_tier"
    tiers:
      - name: "Emerging"
        artworks: 5
      - name: "Established"
        artworks: 20
      - name: "Master"
        artworks: 100
```

---

## 与传统Registry的对比

| 维度 | 传统Registry | BCPP Registry |
|------|-------------|----------------|
| **所有权** | 公司/组织 | 无（公共财产） |
| **注册** | 需要审批 | 无需许可 |
| **修改** | 需要官方 |  Fork即可 |
| **存储** | 中心化服务器 | 去中心化 |
| **身份** | 需要邮箱/账号 | 加密密钥 |
| **争议** | 官方裁决 | 社区投票 |

---

## 路线图

### Phase 1: 基础层 (v1.7.0)
- [x] Registry数据结构定义
- [x] 签名机制
- [ ] 基础SDK
- [ ] CLI工具

### Phase 2: 社区层 (v1.8.0)
- [ ] 提案系统
- [ ] 投票机制
- [ ] 争议解决流程
- [ ] 激励机制

### Phase 3: 生态层 (v2.0.0)
- [ ] 去中心化存储集成
- [ ] ENS/DNSLink解析
- [ ] 跨链作品证明
- [ ] 商业化接口

---

*BCPP Registry - 让艺术协议属于每一个人*
