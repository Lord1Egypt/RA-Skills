# BCPP - Canvas Poetry Protocol
## 画布诗意协议 | v1.7.0

> BCPP = Canvas Poetry Protocol
> 浏览器原生艺术的乐谱标准

---

## 核心理念

**画布即表演**

每一件画布艺术作品都是一场微型戏剧：有开场、发展、高潮、尾声。
BCPP不是配置文件格式，而是**艺术作品的表演脚本**。

---

## 核心原则

1. **极简核心**：协议主体不超过100行
2. **扩展丰富**：复杂性通过扩展机制实现
3. **艺术导向**：每个设计决策都服务于美学表达
4. **时间维度**：艺术是时间轴上的表演，不是静态快照

---

## 协议结构（简化版）

```yaml
# BCPP Manifest - 极简核心
version: "1.7.0"

# ═══════════════════════════════════════════════════════════
# 意图层 (Intention) - 艺术概念
# ═══════════════════════════════════════════════════════════
intention:
  concept: "自然与人文的和谐共生"
  style: "shuimohua"
  mood: ["壮丽", "孤独", "宁静"]
  constraints:
    - "计白当黑"
    - "禁用高饱和度"

# ═══════════════════════════════════════════════════════════
# 描述层 (Descriptor) - 视觉元素
# ═══════════════════════════════════════════════════════════
elements:
  - id: "sky"
    type: "gradient"
    stops: [{p:0,c:"#2a1f4e"},{p:0.6,c:"#c44569"},{p:1,c:"#1a1a2e"}]
  - id: "duck"
    type: "silhouette"
    shape: "bird_flying"
    animation: {path:"arc",duration:12000}

# ═══════════════════════════════════════════════════════════
# 表演层 (Performance) - 时间轴演绎
# ═══════════════════════════════════════════════════════════
performance:
  total_duration: 30000  # 30秒完整演绎
  acts:
    - name: "序章"
      start: 0
      elements: [{id:"sky",fade_in:2000}]
    - name: "发展"
      start: 2000
      elements: [{id:"duck",enter:"left"}]
    - name: "高潮"
      start: 15000
      trigger: "click"  # 用户点击触发
      elements: [{id:"duck",effect:"surprise"}]
    - name: "尾声"
      start: 25000
      elements: [{id:"sky",fade_out:5000}]

# ═══════════════════════════════════════════════════════════
# 渲染层 (Renderer) - 平台适配
# ═══════════════════════════════════════════════════════════
render:
  platform: "web"  # web | eink | spatial | native
  engine: "webgl"
  features: ["particles","glow_effects"]

# ═══════════════════════════════════════════════════════════
# 交互层 (Interaction) - 行为映射
# ═══════════════════════════════════════════════════════════
interaction:
  - trigger: "click"
    target: "water"
    effect: "ripple"
  - trigger: "hover"
    target: "duck"
    effect: "glow"
```

---

## 完整Manifest示例

```yaml
# manifest.yaml —— BCPP艺术作品标准格式
# v1.7.0 - 极简核心版

version: "1.7.0"
protocol: "bcpp"

# ═══════════════════════════════════════════════════════════
# 元数据
# ═══════════════════════════════════════════════════════════
metadata:
  title: "落霞与孤鹜齐飞"
  author: "BCPP-Orchestrator"
  created: "2024-01-15T10:30:00Z"
  genre: "tang_poetry"  # 艺术流派标签
  collection: "唐诗意境系列"

# ═══════════════════════════════════════════════════════════
# 意图层 (Intention Layer)
# ═══════════════════════════════════════════════════════════
intention:
  # 艺术概念
  concept:
    primary: "自然与人文的和谐共生"
    secondary: ["壮美", "孤独", "宁静"]
    keywords: ["落霞", "孤鹜", "秋水", "长天"]

  # 风格定位
  style:
    primary: "shuimohua"  # 水墨画派
    secondary: ["impressionist", "zen"]
    constraints:
      - "计白当黑"
      - "气韵生动"
      - "留白哲学"

  # 情感基调
  mood:
    keywords: ["壮丽", "孤独", "宁静", "深远"]
    intensity: 0.8
    arc:  # 情感曲线
      - time: 0
        emotion: "壮丽"
      - time: 0.5
        emotion: "孤独"
      - time: 1
        emotion: "宁静"

  # 约束条件
  constraints:
    color_palette: ["#2a1f4e","#c44569","#f8b500","#1a1a2e"]
    motion:
      max_velocity: 2.0
      easing: "ease-in-out"
    composition:
      balance: "asymmetric"
      focal_point: {x:0.3,y:0.4}

# ═══════════════════════════════════════════════════════════
# 描述层 (Descriptor Layer)
# ═══════════════════════════════════════════════════════════
descriptor:
  # 视觉元素
  elements:
    - id: "sky_gradient"
      type: "background"
      z_index: 0
      render: "gradient"
      config:
        direction: "vertical"
        stops:
          - position: 0
            color: "#2a1f4e"
            opacity: 1.0
          - position: 0.4
            color: "#c44569"
            opacity: 0.9
          - position: 0.6
            color: "#f8b500"
            opacity: 0.7
          - position: 1
            color: "#1a1a2e"
            opacity: 1.0

    - id: "sunset_haze"
      type: "particle"
      z_index: 1
      count: 50
      color: "#ff6b9d"
      opacity: 0.3
      behavior: "floating"

    - id: "water_surface"
      type: "reflection"
      z_index: 2
      reflection_intensity: 0.4
      wave_amplitude: 5

    - id: "lonely_duck"
      type: "silhouette"
      z_index: 3
      shape: "bird_flying"
      color: "#1a1a2e"

  # 光照配置
  lighting:
    ambient:
      color: "#ffd4a3"
      intensity: 0.6
    directional:
      source: "west"
      color: "#ff8c42"
      intensity: 0.8

  # 后期处理
  post_processing:
    - effect: "vignette"
      intensity: 0.4
    - effect: "color_grade"
      shadows: "#1a1a2e"
      highlights: "#f8b500"
    - effect: "film_grain"
      intensity: 0.1

# ═══════════════════════════════════════════════════════════
# 表演层 (Performance Layer) - 时间轴演绎
# v1.7.0 新增：画布即表演
# ═══════════════════════════════════════════════════════════
performance:
  # 总时长
  duration: 30000  # 30秒

  # 幕次定义
  acts:
    # 第一幕：开场
    - name: "序章"
      start: 0
      duration: 5000
      description: "天空渐显，落霞初现"
      actions:
        - action: "fade_in"
          target: "sky_gradient"
          duration: 3000
          easing: "ease-out"
        - action: "spawn"
          target: "sunset_haze"
          duration: 2000
          delay: 1000

    # 第二幕：发展
    - name: "发展"
      start: 5000
      duration: 10000
      description: "孤鹜入场，秋水映天"
      actions:
        - action: "enter"
          target: "lonely_duck"
          duration: 3000
          path: "arc"
          from: "left"
        - action: "fade_in"
          target: "water_surface"
          duration: 2000
          delay: 2000

    # 第三幕：高潮
    - name: "高潮"
      start: 15000
      duration: 10000
      description: "飞鸟掠影，余晖满天"
      trigger: "auto"  # 自动触发
      actions:
        - action: "animate"
          target: "lonely_duck"
          duration: 10000
          path: "arc"
          loop: true
        - action: "pulse"
          target: "sky_gradient"
          duration: 5000
          intensity: 0.2
        - action: "intensify"
          target: "sunset_haze"
          count: 100
          duration: 5000

    # 第四幕：尾声
    - name: "尾声"
      start: 25000
      duration: 5000
      description: "渐隐归于宁静"
      trigger: "auto"
      actions:
        - action: "fade_out"
          target: "sky_gradient"
          duration: 3000
        - action: "fade_out"
          target: "sunset_haze"
          duration: 2000
        - action: "exit"
          target: "lonely_duck"
          duration: 2000
          to: "right"

  # 循环配置
  loop:
    enabled: true
    mode: "seamless"  # seamless | restart | reverse
    count: null  # null = 无限循环

  # 情感曲线（可选，用于音乐配合）
  emotional_curve:
    - time: 0.0
      emotion: "期待"
      intensity: 0.3
    - time: 0.3
      emotion: "壮丽"
      intensity: 0.9
    - time: 0.5
      emotion: "孤独"
      intensity: 0.7
    - time: 0.8
      emotion: "宁静"
      intensity: 0.5
    - time: 1.0
      emotion: "超脱"
      intensity: 0.2

# ═══════════════════════════════════════════════════════════
# 渲染层 (Renderer Layer)
# ═══════════════════════════════════════════════════════════
render:
  # 目标平台
  platform: "web"

  # 渲染引擎
  engine: "webgl"
  config:
    fps: 60
    responsive: true
    pixel_ratio: "auto"

  # 特性支持
  features:
    - "particles"
    - "fluid_simulation"
    - "glow_effects"
    - "blur"

  # 降级策略
  fallback:
    engine: "canvas_2d"
    features: ["particles","glow_effects"]
    reason: "浏览器不支持WebGL"

  # 平台特定配置
  platform_config:
    web:
      canvas_size: "fullscreen"
      cursor: "none"
    eink:
      grayscale: true
      colors: 4
      dithering: "atkinson"
    spatial:
      depth: true
      environment: "ar"

# ═══════════════════════════════════════════════════════════
# 交互层 (Interaction Layer)
# ═══════════════════════════════════════════════════════════
interaction:
  # 输入类型
  input_types:
    - type: "mouse"
      events: ["move", "click", "scroll"]
    - type: "touch"
      events: ["tap", "swipe"]
    - type: "keyboard"
      events: ["space", "enter"]

  # 交互映射
  mappings:
    - trigger: "mouse_move"
      target: "cursor"
      effect: "glow_follow"
      params:
        radius: 50
        color: "#ffd700"

    - trigger: "click"
      target: "water_surface"
      effect: "ripple"
      params:
        count: 3
        max_radius: 100

    - trigger: "click"
      target: "lonely_duck"
      effect: "reaction"
      params:
        animation: "surprise"
        duration: 500

    - trigger: "scroll"
      target: "camera"
      effect: "parallax"
      params:
        depth: 0.3

  # 行为定义
  behaviors:
    - entity: "lonely_duck"
      states:
        - name: "flying"
          continuous: true
          path: "arc"
          speed: 0.5
        - name: "curious"
          trigger: "mouse_near"
          duration: 2000
          action: "head_turn"
        - name: "resting"
          trigger: "inactive_10s"
          duration: 5000
          action: "hover"

    - entity: "sunset_haze"
      states:
        - name: "floating"
          continuous: true
          variation: "perlin_noise"

# ═══════════════════════════════════════════════════════════
# 画布考古学 (Canvas Archaeology)
# v1.7.0 新增：记录作品历史
# ═══════════════════════════════════════════════════════════
archaeology:
  # 创作历史
  history:
    created:
      timestamp: "2024-01-15T10:30:00Z"
      generator: "BCPP-Orchestrator/1.0"
      source_poem: "落霞与孤鹜齐飞，秋水共长天一色"

    versions:
      - version: "1.0"
        date: "2024-01-15"
        changelog: "Initial creation"
      - version: "1.1"
        date: "2024-01-20"
        changelog: "Added performance layer"

    edits:
      - timestamp: "2024-01-16T14:30:00Z"
        editor: "水墨@1.5"
        change: "调整天空渐变色彩"
      - timestamp: "2024-01-17T09:15:00Z"
        editor: "丹青@1.5"
        change: "优化孤鹜飞行动画"

  # 渲染历史
  render_history:
    - timestamp: "2024-01-15T11:00:00Z"
      platform: "web"
      engine: "webgl"
      browser: "Chrome 120"
      duration_ms: 2500
    - timestamp: "2024-01-16T10:30:00Z"
      platform: "eink"
      engine: "canvas_2d"
      device: "Kindle Paperwhite"
      duration_ms: 5200

  # 观看历史
  view_history:
    - timestamp: "2024-01-15T12:00:00Z"
      viewer: "anon_001"
      duration: 45000
      interactions: 12
      emotion_peak: "壮丽"
    - timestamp: "2024-01-16T14:00:00Z"
      viewer: "anon_002"
      duration: 30000
      interactions: 5
      emotion_peak: "宁静"

  # 签名信息
  signature:
    algorithm: "ed25519"
    creator_key: "bcpp1...abc123"  # Base58编码的公钥
    digest: "sha256_of_manifest"
    timestamp: "2024-01-15T10:30:00Z"

# ═══════════════════════════════════════════════════════════
# 扩展字段
# ═══════════════════════════════════════════════════════════
extensions:
  # 音频配合
  audio:
    - name: "背景音乐"
      url: "assets/bgm_piano.mp3"
      volume: 0.3
      fade_in: 2000
      loop: true

  # 空间音频位置
  spatial_audio:
    - source: "bell"
      position: {x: 3, y: 1, z: -5}
      distance: 10

  # 自定义属性（允许任意扩展）
  custom:
    dedication: "致追求美的人"
    inspiration: "王勃《滕王阁序》"
```

---

## 分层详解

### 1. 意图层 (Intention)

**职责**：定义艺术想要表达什么

```yaml
intention:
  concept:
    primary: "核心概念"
    secondary: ["相关概念1", "相关概念2"]
  style: "shuimohua"  # 流派标签
  mood:
    keywords: ["情感词1", "情感词2"]
    intensity: 0.8
    arc: [{time:0,emotion:"期待"},{time:1,emotion:"超脱"}]
```

### 2. 描述层 (Descriptor)

**职责**：定义视觉元素的结构

```yaml
elements:
  - id: "unique_id"
    type: "gradient|particle|silhouette|..."
    z_index: 0
    # ...类型特定配置
```

### 3. 表演层 (Performance) ⭐ 新增

**职责**：定义时间轴上的演绎

```yaml
performance:
  duration: 30000
  acts:
    - name: "序章"
      start: 0
      trigger: "auto"
      actions:
        - action: "fade_in"
          target: "sky"
  loop:
    enabled: true
    mode: "seamless"
```

### 4. 渲染层 (Renderer)

**职责**：选择合适的渲染引擎

```yaml
render:
  platform: "web|eink|spatial|native"
  engine: "webgl"
  fallback:
    engine: "canvas_2d"
```

### 5. 交互层 (Interaction)

**职责**：定义用户如何参与艺术

```yaml
interaction:
  mappings:
    - trigger: "click"
      target: "water"
      effect: "ripple"
  behaviors:
    - entity: "duck"
      states:
        - name: "flying"
          continuous: true
```

---

## TypeScript 接口定义

```typescript
// BCPP Core Types v1.7.0

export interface BCPPManifest {
  version: string;
  protocol: string;
  metadata?: Metadata;
  intention: Intention;
  descriptor: Descriptor;
  performance: Performance;
  render: Render;
  interaction: Interaction;
  archaeology?: Archaeology;
  extensions?: Record<string, any>;
}

// 意图层
export interface Intention {
  concept: {
    primary: string;
    secondary?: string[];
    keywords?: string[];
  };
  style: {
    primary: string;
    secondary?: string[];
    constraints?: string[];
  };
  mood: {
    keywords: string[];
    intensity: number;
    arc?: EmotionPoint[];
  };
  constraints?: {
    color_palette?: string[];
    motion?: MotionConstraints;
    composition?: CompositionRules;
  };
}

export interface EmotionPoint {
  time: number;
  emotion: string;
  intensity?: number;
}

// 表演层
export interface Performance {
  duration: number;
  acts: Act[];
  loop?: {
    enabled: boolean;
    mode: 'seamless' | 'restart' | 'reverse';
    count?: number;
  };
  emotional_curve?: EmotionPoint[];
}

export interface Act {
  name: string;
  start: number;
  duration?: number;
  description?: string;
  trigger: 'auto' | 'user_interaction' | 'time_absolute' | 'event';
  actions: PerformanceAction[];
}

export interface PerformanceAction {
  action: 'fade_in' | 'fade_out' | 'enter' | 'exit' | 'animate' | 'pulse' | 'spawn' | 'despawn';
  target: string;
  duration?: number;
  delay?: number;
  easing?: string;
  // ... 其他参数
}

// 渲染层
export interface Render {
  platform: 'web' | 'eink' | 'spatial' | 'native';
  engine: string;
  config?: RenderConfig;
  features?: string[];
  fallback?: FallbackConfig;
  platform_config?: Record<string, any>;
}

// 交互层
export interface Interaction {
  input_types: InputType[];
  mappings: InteractionMapping[];
  behaviors?: Behavior[];
}

export interface InteractionMapping {
  trigger: string;
  target: string;
  effect: string;
  params?: Record<string, any>;
}

// 画布考古学
export interface Archaeology {
  history: {
    created: CreationInfo;
    versions?: VersionRecord[];
    edits?: EditRecord[];
  };
  render_history?: RenderRecord[];
  view_history?: ViewRecord[];
  signature?: Signature;
}
```

---

## 艺术流派参考

BCPP不强制流派，但推荐以下流派标签：

| 流派 | 标签 | 特点 |
|------|------|------|
| 水墨画 | `shuimohua` | 计白当黑、墨分五色 |
| 留白派 | `liubai` | 大量空白、极简主义 |
| 粒子派 | `particle` | 以粒子系统为核心 |
| 声响派 | `soundscape` | 以Web Audio为核心 |
| 物理派 | `physics` | 以物理引擎为核心 |
| 赛博朋克 | `cyberpunk` | 霓虹、暗调、科技感 |
| 极光派 | `aurora` | 渐变、光晕、自然光效 |
| 禅意派 | `zen` | 静谧、内省、冥想感 |

---

## 浏览器艺术的美学原则

1. **时间即内容**：艺术在时间轴上展开，观看即参与
2. **交互即诠释**：用户行为是艺术的二次创作
3. **留白为上**：空白不是缺失，是呼吸
4. **气韵流动**：动画应该像呼吸，有自然的节奏
5. **触感真实**：交互应该有重量感、真实感

---

*BCPP - 让浏览器成为画廊，让每一次渲染都是展览*
