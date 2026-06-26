# BCPP Protocol Examples
## 浏览器画布诗意协议 - 示例集 | v1.6.2

---

## 示例概览

本文件提供BCPP协议的实际使用示例，从简单到复杂，涵盖各种艺术场景。

| 示例 | 复杂度 | 描述 |
|------|--------|------|
| 示例1 | ⭐ | 极简：单色渐变 + 点击涟漪 |
| 示例2 | ⭐⭐ | 经典：水墨山水 + 鼠标交互 |
| 示例3 | ⭐⭐⭐ | 完整：唐诗意境 + 多智能体协同 |
| 示例4 | ⭐⭐⭐⭐ | 高级：多目标渲染 + 状态机 |
| 示例5 | ⭐⭐⭐⭐ | 跨平台：Web → E-ink → Spatial |

---

## 示例1：极简涟漪

### 场景
用户输入："一滴水落入平静的湖面"

### manifest.yaml

```yaml
version: "1.6.2"
protocol: "browser-canvas-poetry/bcpp-1.6"

# ═══════════════════════════════════════════════════════════
# 源数据层
# ═══════════════════════════════════════════════════════════
source:
  type: "visual_concept"
  text: "一滴水落入平静的湖面"
  language: "zh-modern"

  semantics:
    imagery:
      - entity: "水"
        visual: "涟漪扩散"
        motion: "圆环向外"
        emotion: "宁静"
      - entity: "湖面"
        visual: "镜面倒影"
        motion: "微光闪烁"
        emotion: "平和"

# ═══════════════════════════════════════════════════════════
# 意图层
# ═══════════════════════════════════════════════════════════
intention:
  concept:
    primary: "瞬间的永恒"
    secondary: ["宁静", "扩散", "循环"]

  style:
    primary: "minimalist"
    secondary: ["zen"]
    constraints:
      - "极简主义"
      - "单色系"

  mood:
    keywords: ["宁静", "平和", "内省"]
    intensity: 0.6

  constraints:
    color_restrictions:
      - "仅用蓝灰调"
      - "禁用鲜艳色"

# ═══════════════════════════════════════════════════════════
# 智能体层
# ═══════════════════════════════════════════════════════════
agents:
  ink_wash:
    role: "atmospheric"
    principles: ["less is more", "留白"]
    constraints: ["极简"]
    output_type: "atmosphere_map"

  pigment:
    role: "interactive"
    principles: ["单点交互"]
    constraints: ["响应 < 50ms"]
    output_type: "composition_tree"

# ═══════════════════════════════════════════════════════════
# 描述层
# ═══════════════════════════════════════════════════════════
descriptor:
  visual:
    background:
      type: "solid"
      color: "#1a2a3a"
      opacity: 1.0

    elements:
      - id: "ripple_center"
        type: "circle"
        initial_radius: 0
        max_radius: 200
        stroke: "#4a6a8a"
        stroke_width: 1

      - id: "ripple_wave_1"
        type: "circle"
        stroke: "#3a5a7a"
        stroke_width: 0.5
        opacity: 0.8

      - id: "ripple_wave_2"
        type: "circle"
        stroke: "#2a4a6a"
        stroke_width: 0.3
        opacity: 0.6

      - id: "ripple_wave_3"
        type: "circle"
        stroke: "#1a3a5a"
        stroke_width: 0.2
        opacity: 0.4

  animation:
    timeline:
      - time: 0
        action: "ripple_spawn"
        duration: 0
      - time: 0
        action: "ripple_expand"
        duration: 3000
        easing: "ease-out"

# ═══════════════════════════════════════════════════════════
# 渲染层
# ═══════════════════════════════════════════════════════════
render:
  targets:
    - id: "browser_canvas"
      engine: "html5_canvas"
      config:
        fps: 60
        responsive: true

  config:
    quality: "medium"

# ═══════════════════════════════════════════════════════════
# 交互层
# ═══════════════════════════════════════════════════════════
interaction:
  input_types:
    - type: "mouse"
      events: ["click"]

  mappings:
    - trigger: "click"
      target: "ripple_center"
      effect: "ripple_spawn"
      params:
        position: "mouse"
        max_radius: 200

  behaviors:
    - entity: "ripple_wave"
      states:
        - name: "expanding"
          continuous: true
          animation: "radius_increase"
          speed: 66  # pixels per second

# ═══════════════════════════════════════════════════════════
# 验证层
# ═══════════════════════════════════════════════════════════
validation:
  weight_normalization: "auto"
  criteria:
    - id: "rhythm_presence"
      importance: 3
      threshold: 0.8
    - id: "minimalist_coherence"
      importance: 4
      threshold: 0.9
    - id: "interaction_responsiveness"
      importance: 3
      threshold: 0.95

  min_score: 0.8
```

### 渲染代码参考

```javascript
// Canvas涟漪实现
class RippleEffect {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.ripples = [];
  }

  createRipple(x, y) {
    this.ripples.push({
      x, y,
      radius: 0,
      maxRadius: 200,
      speed: 66
    });
  }

  update(deltaTime) {
    this.ripples.forEach(r => {
      r.radius += r.speed * deltaTime / 1000;
      r.opacity = 1 - (r.radius / r.maxRadius);
    });
    this.ripples = this.ripples.filter(r => r.radius < r.maxRadius);
  }

  render() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    this.ripples.forEach(r => {
      this.ctx.beginPath();
      this.ctx.arc(r.x, r.y, r.radius, 0, Math.PI * 2);
      this.ctx.strokeStyle = `rgba(74, 106, 138, ${r.opacity})`;
      this.ctx.lineWidth = 1;
      this.ctx.stroke();
    });
  }
}
```

---

## 示例2：水墨山水

### 场景
用户输入："山居秋暝，空山新雨后，天气晚来秋"

### manifest.yaml

```yaml
version: "1.6.2"
protocol: "browser-canvas-poetry/bcpp-1.6"

# ═══════════════════════════════════════════════════════════
# 源数据层
# ═══════════════════════════════════════════════════════════
source:
  type: "poem"
  text: "空山新雨后，天气晚来秋。明月松间照，清泉石上流。"
  language: "zh-classical"
  author: "王维"
  era: "tang"

  semantics:
    imagery:
      - entity: "空山"
        visual: "层叠山峦"
        motion: "云雾缭绕"
        emotion: "空灵"
      - entity: "新雨"
        visual: "湿润感"
        motion: "滴落"
        emotion: "清新"
      - entity: "明月"
        visual: "圆形光晕"
        motion: "静谧"
        emotion: "皎洁"
      - entity: "清泉"
        visual: "流动线条"
        motion: "潺潺"
        emotion: "灵动"

    rhythm:
      meter: "五言律诗"
      pacing: "舒缓"
      caesura: [4, 8]

# ═══════════════════════════════════════════════════════════
# 意图层
# ═══════════════════════════════════════════════════════════
intention:
  concept:
    primary: "天人合一的禅意境界"
    secondary: ["空灵", "清新", "静谧"]

  style:
    primary: "shuimohua"
    secondary: ["zen", "ink_wash"]
    constraints:
      - "计白当黑"
      - "墨分五色"
      - "留白为上"

  mood:
    keywords: ["空灵", "清新", "静谧", "禅意"]
    intensity: 0.7

  constraints:
    color_restrictions:
      - "主色：墨黑、灰白"
      - "点缀：月黄、水蓝"
      - "禁用饱和色"
    motion:
      max_velocity: 1.0
      easing: "ease-in-out-sine"

# ═══════════════════════════════════════════════════════════
# 智能体层
# ═══════════════════════════════════════════════════════════
agents:
  ink_wash:
    role: "atmospheric"
    personality: "成熟、知性、高雅"
    principles:
      - "计白当黑"
      - "气韵生动"
      - "墨分五色"
    constraints:
      - "禁用高饱和度"
      - "最小对比度 1.5:1"
      - "山峦层次3-5层"
    output_type: "atmosphere_map"
    output:
      fields:
        - name: "mountain_layers"
          type: "path_collection"
          count: 4
        - name: "mist_density"
          type: "heatmap"
          animation: "floating"
        - name: "ink_pressure"
          type: "2d_array"
          description: "墨色浓淡分布"

  pigment:
    role: "interactive"
    personality: "萝莉、灵动、活泼、可爱"
    principles:
      - "随类赋彩"
      - "点睛之笔"
      - "活泼灵动"
    constraints:
      - "仅用月黄与水蓝作为点缀"
      - "交互要轻盈"
    output_type: "composition_tree"
    output:
      fields:
        - name: "color_palette"
          type: "palette"
          colors: ["#1a1a2e", "#3a3a5e", "#8a8aae", "#f8e8a0", "#a0c8e8"]
        - name: "highlight_points"
          type: "position_set"
          description: "高光点（萤火虫、月亮、水珠）"

  orchestrator:
    role: "coordination"
    responsibilities:
      - "整合水墨山峦与丹青点缀"
      - "保持禅意空灵的整体感"

# ═══════════════════════════════════════════════════════════
# 描述层
# ═══════════════════════════════════════════════════════════
descriptor:
  visual:
    background:
      type: "gradient"
      config:
        direction: "vertical"
        stops:
          - position: 0
            color: "#2a3a4a"
            opacity: 1.0
          - position: 0.3
            color: "#4a5a6a"
            opacity: 1.0
          - position: 0.5
            color: "#6a7a8a"
            opacity: 1.0
          - position: 1
            color: "#1a2a3a"
            opacity: 1.0

    elements:
      - id: "mountains_back"
        type: "mountain_layer"
        color: "#3a3a5e"
        opacity: 0.6
        position: { x: 0, y: 0.3 }
        height_ratio: 0.4

      - id: "mountains_mid"
        type: "mountain_layer"
        color: "#2a2a4e"
        opacity: 0.8
        position: { x: 0, y: 0.4 }
        height_ratio: 0.35

      - id: "mountains_front"
        type: "mountain_layer"
        color: "#1a1a2e"
        opacity: 1.0
        position: { x: 0, y: 0.5 }
        height_ratio: 0.4

      - id: "mist_layer"
        type: "particle"
        count: 30
        color: "rgba(200, 200, 220, 0.3)"
        behavior: "floating"
        position: { y: 0.4 }
        height: 0.2

      - id: "moon"
        type: "circle"
        radius: 30
        position: { x: 0.8, y: 0.15 }
        color: "#f8e8a0"
        glow: true
        glow_radius: 60
        glow_color: "rgba(248, 232, 160, 0.3)"

      - id: "moonlight"
        type: "gradient"
        config:
          type: "radial"
          center: { x: 0.8, y: 0.15 }
          radius: 200
          stops:
            - position: 0
              color: "rgba(248, 232, 160, 0.4)"
            - position: 1
              color: "rgba(248, 232, 160, 0)"

      - id: "stream"
        type: "path"
        path_type: "bezier"
        control_points:
          - { x: 0.3, y: 0.7 }
          - { x: 0.4, y: 0.65 }
          - { x: 0.5, y: 0.72 }
          - { x: 0.6, y: 0.68 }
          - { x: 0.7, y: 0.75 }
        stroke: "#5a7a9a"
        stroke_width: 8
        animated: true
        flow_speed: 0.5

      - id: "fireflies"
        type: "particle"
        count: 8
        color: "#f8e8a0"
        size: 3
        behavior: "float"
        opacity: 0.6
        positions:
          - { x: 0.3, y: 0.5 }
          - { x: 0.5, y: 0.45 }
          - { x: 0.65, y: 0.55 }

    lighting:
      ambient:
        color: "#a0a0b0"
        intensity: 0.4
      point_lights:
        - position: { x: 0.8, y: 0.15 }
          color: "#f8e8a0"
          intensity: 0.6
          falloff: 0.2

    post_processing:
      - effect: "vignette"
        intensity: 0.5
        smoothness: 0.8
      - effect: "film_grain"
        intensity: 0.08
      - effect: "ink_texture"
        intensity: 0.15

  animation:
    timeline:
      - time: 0
        action: "fade_in"
        duration: 3000
        elements: ["mountains_back", "mountains_mid"]
      - time: 2000
        action: "fade_in"
        duration: 2000
        elements: ["mountains_front", "moon", "moonlight"]
      - time: 4000
        action: "start_loop"
        elements: ["mist_layer", "fireflies", "stream"]

      global_settings:
        fps: 30
        easing: "ease-in-out-sine"

# ═══════════════════════════════════════════════════════════
# 渲染层
# ═══════════════════════════════════════════════════════════
render:
  targets:
    - id: "browser_canvas"
      priority: 1
      engine: "canvas_2d"
      config:
        fps: 30
        responsive: true
        pixel_ratio: "auto"

    - id: "e_ink_display"
      priority: 2
      engine: "canvas_2d"
      config:
        grayscale: true
        dithering: "atkinson"

  config:
    quality: "high"
    anti_aliasing: true

  output:
    format: "single_html"
    includes:
      - "index.html"
      - "style.css"
      - "main.js"

# ═══════════════════════════════════════════════════════════
# 交互层
# ═══════════════════════════════════════════════════════════
interaction:
  input_types:
    - type: "mouse"
      events: ["move", "click"]
    - type: "touch"
      events: ["tap"]

  mappings:
    - trigger: "mouse_move"
      target: "cursor_area"
      effect: "firefly_attract"
      params:
        radius: 80
        attraction_strength: 0.3

    - trigger: "click_on_moon"
      target: "moon"
      effect: "pulse_glow"
      params:
        duration: 1000
        scale: 1.2

    - trigger: "click_on_stream"
      target: "stream"
      effect: "ripple"
      params:
        ripple_count: 2
        max_radius: 30

  behaviors:
    - entity: "fireflies"
      states:
        - name: "floating"
          continuous: true
          animation: "perlin_walk"
          area: { x: [0.2, 0.8], y: [0.4, 0.7] }
          speed: 0.3
        - name: "attracted"
          trigger: "mouse_near"
          duration: 1500
          animation: "move_toward"
          strength: 0.5

    - entity: "mist"
      states:
        - name: "drifting"
          continuous: true
          animation: "horizontal_float"
          speed: 0.1
          opacity_variation: 0.2

    - entity: "stream"
      states:
        - name: "flowing"
          continuous: true
          animation: "flow_animation"
          speed: 0.5

  state_machine:
    initial: "intro"
    states:
      - name: "intro"
        duration: 5000
        animation: "fade_in_sequence"
        transitions:
          - to: "interactive"
            condition: "time_elapsed"
      - name: "interactive"
        type: "steady"
        transitions:
          - to: "focus_mode"
            condition: "click_on_element"
      - name: "focus_mode"
        duration: 3000
        transitions:
          - to: "interactive"
            condition: "click_outside"

# ═══════════════════════════════════════════════════════════
# 验证层
# ═══════════════════════════════════════════════════════════
validation:
  criteria:
    - id: "ink_wash_coherence"
      weight: 0.4
      description: "是否保持水墨画的留白美学"
      check: "contrast_ratio_and_color_restriction"
      threshold: 0.85

    - id: "imagery_fidelity"
      weight: 0.3
      description: "山、月、水、萤火虫意象是否完整"
      check: "element_coverage"
      threshold: 0.8

    - id: "zen_atmosphere"
      weight: 0.3
      description: "整体是否有禅意空灵感"
      check: "motion_smoothing_and_pacing"
      threshold: 0.75

  min_score: 0.8
```

---

## 示例3：唐诗意境（完整）

### 场景
用户输入："春江花月夜"（张若虚）

```yaml
version: "1.6.2"
protocol: "browser-canvas-poetry/bcpp-1.6"

# ═══════════════════════════════════════════════════════════
# 源数据层
# ═══════════════════════════════════════════════════════════
source:
  type: "poem"
  text: |
    春江潮水连海平，海上明月共潮生。
    滟滟随波千万里，何处春江无月明。
  language: "zh-classical"
  author: "张若虚"
  era: "tang"
  title: "春江花月夜"

  semantics:
    imagery:
      - entity: "春江"
        visual: "宽阔水面"
        motion: "潮起潮落"
        emotion: "壮阔"
      - entity: "明月"
        visual: "圆形光球"
        motion: "随波升起"
        emotion: "皎洁"
      - entity: "滟滟"
        visual: "波光粼粼"
        motion: "闪烁流动"
        emotion: "绮丽"
      - entity: "千万里"
        visual: "无限延伸"
        motion: "渐远渐淡"
        emotion: "深远"

    rhythm:
      meter: "歌行体"
      pacing: "前起后伏，悠长连绵"
      caesura: [8, 16]

# ═══════════════════════════════════════════════════════════
# 意图层
# ═══════════════════════════════════════════════════════════
intention:
  concept:
    primary: "宇宙永恒与人生短暂的对照"
    secondary: ["壮阔", "皎洁", "绮丽", "深远", "感慨"]

  style:
    primary: "impressionist_shuimo"
    secondary: ["romantic", "lyrical"]
    constraints:
      - "以形写神"
      - "虚实相生"
      - "气韵流动"

  mood:
    keywords: ["壮阔", "绮丽", "深远", "感慨", "优美"]
    intensity: 0.85
    transitions:
      - from: "壮阔"
        to: "绮丽"
        duration: 5000
      - from: "绮丽"
        to: "感慨"
        duration: 8000

  constraints:
    color_restrictions:
      - "主色：深蓝、靛青、银白"
      - "点缀：暖黄、淡紫"
      - "禁用土色、艳红"
    motion:
      max_velocity: 1.5
      easing: "ease-in-out-sine"
      continuity: 0.9  # 高连续性

# ═══════════════════════════════════════════════════════════
# 智能体层
# ═══════════════════════════════════════════════════════════
agents:
  ink_wash:
    role: "atmospheric"
    personality: "成熟、知性、高雅"
    principles:
      - "计白当黑"
      - "气韵生动"
      - "虚实相生"
    constraints:
      - "山峦或建筑用墨色剪影"
      - "水面用留白表现"
      - "层次3-5层"
    output_type: "atmosphere_map"
    output:
      fields:
        - name: "horizon_line"
          type: "float"
          description: "海平线位置（0-1）"
        - name: "wave_pattern"
          type: "2d_function"
          description: "波浪形态函数"
        - name: "reflection_map"
          type: "2d_array"
          description: "倒影强度分布"

  pigment:
    role: "interactive"
    personality: "萝莉、灵动、活泼、可爱"
    principles:
      - "随类赋彩"
      - "点石成金"
      - "以动衬静"
    constraints:
      - "月光用银白色光晕"
      - "波光用暖黄点缀"
      - "交互要轻盈如风"
    output_type: "composition_tree"
    output:
      fields:
        - name: "color_palette"
          type: "palette"
          colors:
            primary: ["#0a1628", "#1a3a5a", "#2a5a8a"]
            secondary: ["#e8d8a0", "#c8b870", "#a89850"]
            accent: ["#f8e8d0", "#e8d8c0"]
        - name: "light_sources"
          type: "position_set"
          description: "光源位置（主：月亮，次：波光）"

  orchestrator:
    role: "coordination"
    responsibilities:
      - "协调水墨与丹青的输出比例"
      - "保持'静中有动，动中有静'的平衡"
      - "生成完整的art-descriptor"

# ═══════════════════════════════════════════════════════════
# 描述层
# ═══════════════════════════════════════════════════════════
descriptor:
  visual:
    background:
      type: "gradient"
      config:
        direction: "vertical"
        stops:
          - position: 0
            color: "#0a0a1a"
            opacity: 1.0
          - position: 0.3
            color: "#0a1628"
            opacity: 1.0
          - position: 0.5
            color: "#1a2a4a"
            opacity: 1.0
          - position: 0.7
            color: "#1a3a5a"
            opacity: 1.0
          - position: 1
            color: "#0a1628"
            opacity: 1.0

    elements:
      # 天空层
      - id: "night_sky"
        type: "gradient"
        z_index: 0
        config:
          type: "radial"
          center: { x: 0.5, y: 0.25 }
          radius: 0.8
          stops:
            - position: 0
              color: "#2a4a6a"
            - position: 1
              color: "#0a0a1a"

      # 月亮
      - id: "moon"
        type: "circle"
        z_index: 1
        radius: 40
        position: { x: 0.5, y: 0.25 }
        color: "#f8f0e0"
        glow: true
        glow_radius: 120
        glow_color: "rgba(248, 240, 224, 0.3)"
        animation:
          type: "rise"
          duration: 3000
          easing: "ease-out"

      # 月光
      - id: "moonlight_path"
        type: "path"
        z_index: 2
        path_type: "bezier"
        control_points:
          - { x: 0.5, y: 0.3 }
          - { x: 0.5, y: 0.5 }
          - { x: 0.5, y: 0.7 }
          - { x: 0.5, y: 1.0 }
        stroke: "rgba(248, 240, 224, 0.1)"
        stroke_width: 150

      # 波浪层（近景）
      - id: "waves_close"
        type: "wave"
        z_index: 3
        count: 5
        spacing: 40
        y_position: 0.65
        amplitude: 8
        frequency: 0.02
        color: "#1a3a5a"
        opacity: 0.8
        animation:
          type: "horizontal_flow"
          speed: 0.5

      # 波浪层（中景）
      - id: "waves_mid"
        type: "wave"
        z_index: 4
        count: 4
        spacing: 60
        y_position: 0.55
        amplitude: 6
        frequency: 0.015
        color: "#2a4a6a"
        opacity: 0.6
        animation:
          type: "horizontal_flow"
          speed: 0.3

      # 波光粼粼
      - id: "sparkles"
        type: "particle"
        z_index: 5
        count: 100
        color: "#f8e8a0"
        size: { min: 1, max: 4 }
        opacity: { min: 0.3, max: 0.9 }
        positions:
          x_range: [0.2, 0.8]
          y_range: [0.55, 0.9]
        behavior: "twinkle"
        animation:
          type: "random_twinkle"
          duration_range: [500, 2000]

      # 月亮倒影
      - id: "moon_reflection"
        type: "ellipse"
        z_index: 6
        position: { x: 0.5, y: 0.72 }
        radius_x: 35
        radius_y: 80
        color: "#f8f0e0"
        opacity: 0.4
        blur: 10
        animation:
          type: "wave_distort"
          amplitude: 5
          speed: 1.5

    lighting:
      ambient:
        color: "#a0b0c0"
        intensity: 0.3
      point_lights:
        - position: { x: 0.5, y: 0.25 }
          color: "#f8f0e0"
          intensity: 1.0
          falloff: 0.1
          type: "directional_down"

    post_processing:
      - effect: "vignette"
        intensity: 0.6
        smoothness: 0.7
      - effect: "color_grade"
        shadows: "#0a1628"
        midtones: "#1a3a5a"
        highlights: "#f8e8a0"
        saturation: 0.7
      - effect: "bloom"
        intensity: 0.3
        threshold: 0.8
      - effect: "film_grain"
        intensity: 0.06

  animation:
    timeline:
      - time: 0
        action: "fade_in"
        duration: 2000
        elements: ["night_sky"]

      - time: 1000
        action: "moon_rise"
        duration: 3000
        elements: ["moon", "moonlight_path"]

      - time: 3000
        action: "waves_appear"
        duration: 2000
        elements: ["waves_mid", "waves_close"]

      - time: 4000
        action: "sparkles_appear"
        duration: 3000
        elements: ["sparkles", "moon_reflection"]

      - time: 7000
        action: "start_loop"
        elements: ["waves_close", "waves_mid", "sparkles", "moon_reflection"]

      - time: 7000
        action: "continuous"
        elements: ["sparkles"]

    global_settings:
      fps: 30
      smoothing: true
      time_scale: 1.0

# ═══════════════════════════════════════════════════════════
# 渲染层
# ═══════════════════════════════════════════════════════════
render:
  targets:
    - id: "browser_canvas"
      priority: 1
      engine: "webgl"
      config:
        fps: 30
        responsive: true
        pixel_ratio: "auto"
        features:
          - "particle_system"
          - "wave_simulation"
          - "glow_effects"
          - "blur"
      optimization:
        level: "high"
        fallback: "canvas_2d"

    - id: "mobile_webgl"
      priority: 2
      engine: "webgl"
      config:
        fps: 30
        pixel_ratio: 1.0  # 限制分辨率
        features:
          - "particle_system"
          - "glow_effects"

  config:
    quality: "high"
    anti_aliasing: true
    color_space: "srgb"

  output:
    format: "single_html"
    includes:
      - "index.html"
      - "shaders/*.glsl"
    compression: true

# ═══════════════════════════════════════════════════════════
# 交互层
# ═══════════════════════════════════════════════════════════
interaction:
  input_types:
    - type: "mouse"
      events: ["move", "click", "scroll"]
    - type: "touch"
      events: ["tap", "swipe"]
    - type: "keyboard"
      events: ["space"]

  mappings:
    # 鼠标移动产生波光跟随
    - trigger: "mouse_move"
      target: "sparkles"
      effect: "attract_and_twinkle"
      params:
        radius: 100
        sparkle_intensity: 1.5
        duration: 2000

    # 点击水面产生涟漪
    - trigger: "click"
      target: "water"
      effect: "ripple"
      params:
        position: "mouse"
        ripple_count: 5
        max_radius: 80
        decay: 0.92

    # 滚动改变视角
    - trigger: "scroll"
      target: "camera"
      effect: "zoom"
      params:
        min_zoom: 0.5
        max_zoom: 2.0
        sensitivity: 0.001

    # 空格键暂停/播放动画
    - trigger: "keydown_space"
      target: "global"
      effect: "toggle_animation"

  behaviors:
    - entity: "sparkles"
      states:
        - name: "twinkling"
          continuous: true
          animation: "random_twinkle"
          intensity: 0.7
        - name: "attracted"
          trigger: "mouse_near"
          duration: 2000
          animation: "move_and_twinkle"
          attraction: 0.3

    - entity: "waves_close"
      states:
        - name: "flowing"
          continuous: true
          animation: "horizontal_wave"
          speed: 0.5
          amplitude: 8
        - name: "excited"
          trigger: "mouse_click_water"
          duration: 1500
          speed: 2.0
          amplitude: 15

    - entity: "moon"
      states:
        - name: "steady"
          continuous: true
          glow_pulse: 0.1
          pulse_speed: 0.5
        - name: "pulse"
          trigger: "click"
          duration: 1000
          glow_intensity: 1.5

  state_machine:
    initial: "intro"
    states:
      - name: "intro"
        duration: 5000
        animation: "fade_in_sequence"
        transitions:
          - to: "ambient"
            condition: "time_elapsed"
      - name: "ambient"
        type: "steady"
        description: "宁静的夜江花月夜"
        transitions:
          - to: "interactive"
            condition: "user_interaction"
          - to: "dynamic"
            condition: "continuous_interaction"
      - name: "dynamic"
        type: "event_based"
        description: "用户互动时的动态响应"
        transitions:
          - to: "ambient"
            condition: "no_interaction_5s"

# ═══════════════════════════════════════════════════════════
# 验证层
# ═══════════════════════════════════════════════════════════
validation:
  criteria:
    - id: "imagery_coverage"
      weight: 0.3
      description: "春、江、花、月、夜五要素是否完整"
      check: "element_mapping"
      elements: ["春江", "明月", "波光", "夜空"]
      threshold: 0.9

    - id: "emotional_resonance"
      weight: 0.3
      description: "是否传达出诗歌的壮阔与绮丽"
      check: "mood_keywords_matching"
      threshold: 0.8

    - id: "visual_coherence"
      weight: 0.25
      description: "整体视觉是否和谐统一"
      check: "color_harmony_and_contrast"
      threshold: 0.85

    - id: "interaction_quality"
      weight: 0.15
      description: "交互是否自然流畅"
      check: "response_latency_and_effectiveness"
      threshold: 0.9

  min_score: 0.82

  # 艺术评价
  artistic_evaluation:
    style: "impressionist_shuimo"
    evaluation:
      concept: "宇宙永恒与人生短暂的对照"
      execution: "水墨留白与印象派光影的结合"
      highlights:
        - "月光路径的渐变效果"
        - "波光的随机闪烁"
        - "倒影的水波扭曲"
      suggestions:
        - "可加入远处渔火点缀"
        - "可考虑加入诗歌朗诵音频"
```

---

## 示例4：多目标渲染 + 状态机

### 场景
复杂交互艺术作品，支持多种输出目标

```yaml
version: "1.6.2"
protocol: "browser-canvas-poetry/bcpp-1.6"

source:
  type: "visual_concept"
  text: "一座未来城市，人工智能觉醒的夜晚"

intention:
  concept:
    primary: "科技与人性的张力"
    secondary: ["赛博朋克", "孤独", "希望"]

  style:
    primary: "cyberpunk"
    secondary: ["neon", "dark"]

  mood:
    keywords: ["神秘", "孤独", "希望", "紧张"]
    intensity: 0.9

# ═══════════════════════════════════════════════════════════
# 多渲染目标
# ═══════════════════════════════════════════════════════════
render:
  targets:
    - id: "desktop_webgl"
      priority: 1
      engine: "three"
      config:
        fps: 60
        quality: "ultra"
        features:
          - "ray_tracing"
          - "post_processing"
          - "particle_system"

    - id: "mobile_canvas"
      priority: 2
      engine: "canvas_2d"
      config:
        fps: 30
        quality: "medium"
        features:
          - "particles"
          - "glow_effects"

    - id: "e_ink"
      priority: 3
      engine: "canvas_2d"
      config:
        grayscale: true
        colors: 4
        dithering: "atkinson"

# ═══════════════════════════════════════════════════════════
# 复杂状态机
# ═══════════════════════════════════════════════════════════
interaction:
  state_machine:
    initial: "dormant"

    states:
      - name: "dormant"
        description: "城市沉睡，等待唤醒"
        duration: null
        transitions:
          - to: "awakening"
            condition: "first_interaction"
            probability: 1.0

      - name: "awakening"
        description: "城市开始苏醒，灯光渐亮"
        duration: 5000
        animation_sequence:
          - step: 1
            action: "flicker_lights"
            duration: 2000
          - step: 2
            action: "turn_on_signs"
            duration: 2000
          - step: 3
            action: "enable_ai_core"
            duration: 1000
        transitions:
          - to: "alive"
            condition: "animation_complete"
            probability: 1.0

      - name: "alive"
        description: "城市正常运行"
        duration: null
        transitions:
          - to: "focused"
            condition: "click_on_element"
            probability: 0.8
          - to: "emergency"
            condition: "rapid_clicks"
            probability: 0.3

      - name: "focused"
        description: "聚焦某个AI核心"
        duration: 8000
        effects:
          - "zoom_to_element"
          - "show_details"
          - "enable_chat"
        transitions:
          - to: "alive"
            condition: "click_outside"
            probability: 1.0

      - name: "emergency"
        description: "异常行为触发警报"
        duration: 3000
        animation_sequence:
          - step: 1
            action: "flash_red"
            duration: 500
          - step: 2
            action: "sound_alarm"
            duration: 2500
        transitions:
          - to: "recovery"
            condition: "time_elapsed"
            probability: 1.0

      - name: "recovery"
        description: "系统恢复"
        duration: 4000
        animation_sequence:
          - step: 1
            action: "gradual_calm"
            duration: 4000
        transitions:
          - to: "alive"
            condition: "animation_complete"
            probability: 1.0

  # 复杂交互映射
  mappings:
    - trigger: "click_on_core"
      target: "ai_core"
      effect: "focus"
      params:
        zoom_level: 2.0
        show_info: true
        enable_chat: true

    - trigger: "hover_on_light"
      target: "neon_light"
      effect: "intensify"
      params:
        brightness: 1.5
        color_shift: "+10"

    - trigger: "rapid_click"
      target: "city"
      effect: "emergency_protocol"
      params:
        threshold: 5
        interval: 500
```

---

## 示例5：跨平台渲染对比

### 场景
同一首诗《枫桥夜泊》在三种不同平台的渲染方案对比

```yaml
version: "1.6.2"
protocol: "browser-canvas-poetry/bcpp-1.6"

source:
  type: "poem"
  text: "月落乌啼霜满天，江枫渔火对愁眠。姑苏城外寒山寺，夜半钟声到客船。"
  language: "zh-classical"
  author: "张继"
  era: "tang"
  title: "枫桥夜泊"

# ═══════════════════════════════════════════════════════════
# 意图层（跨平台共用）
# ═══════════════════════════════════════════════════════════
intention:
  concept:
    primary: "羁旅之愁与禅意钟声的交融"
    secondary: ["寂寥", "秋寒", "禅意", "愁绪"]
  style:
    primary: "shuimohua"
    constraints:
      - "计白当黑"
      - "墨分五色"
      - "留白为上"
  mood:
    keywords: ["寂寥", "秋寒", "禅意", "愁绪", "悠远"]
    intensity: 0.75

# ═══════════════════════════════════════════════════════════
# 渲染层（多平台目标）
# ═══════════════════════════════════════════════════════════
render:
  targets:
    # 目标1: Web浏览器 - 完整交互体验
    - id: "web_full"
      platform: "web"
      priority: 1
      engine: "webgl"
      config:
        fps: 60
        responsive: true
        features:
          - "particle_system"      # 霜/雾气粒子
          - "glow_effects"        # 渔火光晕
          - "blur"               # 模糊效果
          - "audio"              # 钟声音频
      optimization:
        level: "high"
        fallback: "canvas_2d"
      descriptor_override:
        # Web平台完整描述
        elements:
          - id: "sky_night"
            type: "gradient"
            z_index: 0
            stops:
              - position: 0
                color: "#0a0a1a"
              - position: 0.6
                color: "#1a2a3a"
              - position: 1
                color: "#2a3a4a"
          - id: "moon"
            type: "circle"
            z_index: 1
            radius: 25
            position: { x: 0.7, y: 0.2 }
            color: "#f8f0e0"
            glow: true
            glow_radius: 80
          - id: "crows"
            type: "particle"
            z_index: 2
            count: 5
            color: "#1a1a2e"
            behavior: "flying"
            animation:
              path: "random_walk"
              speed: 0.5
          - id: "frost_particles"
            type: "particle"
            z_index: 3
            count: 200
            color: "rgba(255,255,255,0.3)"
            behavior: "falling"
            animation:
              speed: 0.2
              direction: "diagonal"
          - id: "river"
            type: "wave"
            z_index: 4
            color: "#1a2a3a"
            opacity: 0.8
            animation:
              wave_height: 3
              speed: 0.3
          - id: "fishing_boats"
            type: "silhouette"
            z_index: 5
            count: 3
            shape: "boat"
            positions:
              - { x: 0.3, y: 0.6 }
              - { x: 0.5, y: 0.65 }
              - { x: 0.7, y: 0.58 }
            glow: true
            glow_color: "rgba(255,200,100,0.5)"
          - id: "maple_bridge"
            type: "silhouette"
            z_index: 6
            shape: "bridge_arch"
            position: { x: 0.4, y: 0.55 }
            color: "#1a1a2e"
          - id: "temple"
            type: "silhouette"
            z_index: 7
            shape: "building"
            position: { x: 0.85, y: 0.4 }
            color: "#0a0a1a"
          - id: "bell_sound_waves"
            type: "ring"
            z_index: 8
            trigger: "time_12pm"
            count: 3
            color: "rgba(248,240,224,0.2)"
            animation:
              expand: true
              duration: 3000

    # 目标2: 电子墨水屏 - 降级简化
    - id: "eink_display"
      platform: "eink"
      priority: 2
      engine: "canvas_2d"
      config:
        refresh_mode: "partial"
        grayscale: true
        dithering: "atkinson"
        max_colors: 4
      descriptor_override:
        # E-ink降级策略
        color_mapping:
          "#0a0a1a": "black"
          "#1a2a3a": "dark_gray"
          "#f8f0e0": "light_gray"
          "#2a3a4a": "gray"
        elements:
          - id: "sky"
            type: "solid"
            z_index: 0
            color: "dark_gray"    # 简化为纯色
          - id: "moon"
            type: "circle"
            z_index: 1
            radius: 15            # 缩小
            position: { x: 0.7, y: 0.2 }
            color: "light_gray"
          - id: "fishing_boats"
            type: "silhouette"
            z_index: 2
            count: 3
            shape: "simple_boat"
            color: "black"
          - id: "bridge"
            type: "line"
            z_index: 3
            path: "arch"
            color: "black"
            stroke_width: 2
          - id: "temple"
            type: "rectangle"
            z_index: 4
            position: { x: 0.85, y: 0.4 }
            color: "black"
          # 移除: 粒子效果、动画、模糊、音频
        animation:
          enabled: false         # 禁用动画
        interaction:
          enabled: false         # 禁用交互

    # 目标3: 空间计算 - 沉浸增强
    - id: "spatial_vision"
      platform: "spatial"
      priority: 3
      engine: "realitykit"
      config:
        depth: true
        hand_tracking: true
        environment: "ar"
        immersive: true
      descriptor_override:
        # Spatial增强描述
        elements:
          - id: "sky_sphere"
            type: "3d_environment"
            z_index: 0
            geometry: "sphere"
            color: "#0a0a1a"
            radius: 50
          - id: "moon_3d"
            type: "3d_object"
            z_index: 1
            geometry: "sphere"
            radius: 0.5
            position: { x: 3, y: 2, z: -5 }
            material: "emissive"
            color: "#f8f0e0"
            animation:
              type: "float"
              amplitude: 0.1
          - id: "river_3d"
            type: "3d_surface"
            z_index: 2
            geometry: "plane"
            size: { width: 20, height: 10 }
            position: { x: 0, y: -1, z: -3 }
            material: "reflective"
            color: "#1a2a3a"
            animation:
              wave_height: 0.1
          - id: "boats_3d"
            type: "3d_object"
            z_index: 3
            geometry: "custom_boat"
            count: 3
            positions:
              - { x: -2, y: 0, z: -4 }
              - { x: 0, y: 0, z: -3 }
              - { x: 2, y: 0, z: -4.5 }
            material: "emissive"
            glow_color: "rgba(255,200,100,0.8)"
          - id: "bridge_3d"
            type: "3d_object"
            z_index: 4
            geometry: "arch_bridge"
            position: { x: -1, y: 0.5, z: -3 }
            color: "#1a1a2e"
          - id: "temple_3d"
            type: "3d_object"
            z_index: 5
            geometry: "temple"
            position: { x: 4, y: 0, z: -8 }
            color: "#0a0a1a"
          - id: "frost_volume"
            type: "3d_volume"
            z_index: 6
            geometry: "particles"
            count: 500
            color: "rgba(255,255,255,0.4)"
            bounds: { width: 15, height: 10, depth: 15 }
            animation:
              type: "drifting"
              speed: 0.1
          - id: "bell_3d"
            type: "3d_object"
            z_index: 7
            geometry: "bell"
            position: { x: 4, y: 1, z: -8 }
            material: "metal"
            animation:
              type: "swing"
              trigger: "time_12pm"
              duration: 3000
        spatial:
          player_height: 1.7
          look_range:
            horizontal: 360
            vertical: 120
          interaction_mode: "gaze_and_gesture"

# ═══════════════════════════════════════════════════════════
# 跨平台降级策略配置
# ═══════════════════════════════════════════════════════════
platform_strategy:
  # Web平台降级路径
  web:
    full: "webgl"
    medium: "canvas_2d"
    low: "css_animation"
    fallback_reason: "浏览器兼容性"

  # E-ink平台降级路径
  eink:
    full: "canvas_2d_gray"
    medium: "canvas_2d_dither"
    low: "svg_mono"
    fallback_reason: "墨水屏刷新限制"
    features_removed:
      - "particle_animation"
      - "blur_effects"
      - "audio"

  # Spatial平台降级路径
  spatial:
    full: "realitykit"
    medium: "arkit_webgl"
    low: "360_video"
    fallback_reason: "设备能力差异"

# ═══════════════════════════════════════════════════════════
# 交互层（Web和Spatial平台）
# ═══════════════════════════════════════════════════════════
interaction:
  # Web平台交互
  web:
    input_types:
      - type: "mouse"
        events: ["move", "click", "scroll"]
      - type: "touch"
        events: ["tap", "swipe"]
    mappings:
      - trigger: "click_on_boat"
        target: "fishing_boats"
        effect: "boat_glow_intensify"
        params:
          glow_multiplier: 2
      - trigger: "click_on_temple"
        target: "bell_sound_waves"
        effect: "trigger_bell"
      - trigger: "scroll"
        target: "camera"
        effect: "zoom"
        params:
          range: [0.5, 2.0]

  # Spatial平台交互
  spatial:
    input_types:
      - type: "gaze"
        events: ["enter", "dwell", "exit"]
      - type: "hand"
        events: ["pinch", "grab", "point"]
      - type: "voice"
        commands: ["look at boat", "ring the bell"]
    mappings:
      - trigger: "gaze_dwell_temple"
        target: "bell_3d"
        effect: "swing_bell"
        duration: 1500
      - trigger: "pinch_on_boat"
        target: "boats_3d"
        effect: "move_boat"
        params:
          follow_hand: true

# ═══════════════════════════════════════════════════════════
# 验证层
# ═══════════════════════════════════════════════════════════
validation:
  criteria:
    - id: "imagery_coverage"
      importance: 4
      description: "月、乌、霜、江枫渔火、寒山寺、钟声六要素"
      threshold: 0.9

    - id: "emotional_resonance"
      importance: 4
      description: "羁旅愁绪与禅意钟声的传达"
      threshold: 0.8

    - id: "platform_adaptation"
      importance: 3
      description: "各平台渲染是否合理降级"
      check: "feature_degradation_appropriate"
      threshold: 0.75

    - id: "aesthetic_coherence"
      importance: 3
      description: "水墨留白美学是否保持"
      threshold: 0.85

  # 平台特定验证
  platform_validation:
    web:
      criteria:
        - id: "interaction_responsiveness"
          threshold: 0.9
        - id: "animation_smoothness"
          threshold: 0.85

    eink:
      criteria:
        - id: "contrast_readability"
          threshold: 0.8
        - id: "dithering_quality"
          threshold: 0.75

    spatial:
      criteria:
        - id: "depth_perception"
          threshold: 0.85
        - id: "gesture_recognition"
          threshold: 0.8
```

### 跨平台渲染对比表

| 维度 | Web (WebGL) | E-ink | Spatial (AR) |
|------|-------------|-------|--------------|
| **视觉复杂度** | 完整粒子+动画 | 简化几何 | 3D体积 |
| **色彩** | 全彩渐变 | 4阶灰度 | 全彩+发光 |
| **动画** | 60fps流畅 | 静态 | 3D漂浮 |
| **交互** | 鼠标/触摸 | 无 | 手势/注视 |
| **音频** | 钟声3D音效 | 无 | 空间音频 |
| **沉浸感** | 屏幕内 | 黑白纸张 | 空间环绕 |

### 渲染器实现要点

```typescript
// 跨平台渲染器选择逻辑
function selectRenderer(platform: Platform, capabilities: Capability[]): Renderer {
  switch (platform) {
    case 'web':
      if (capabilities.includes('webgl2')) return new WebGLRenderer();
      if (capabilities.includes('canvas2d')) return new Canvas2DRenderer();
      return new CSSRenderer(); // 最终降级

    case 'eink':
      if (capabilities.includes('grayscale')) return new EInkRenderer({
        colors: 4,
        dithering: 'atkinson'
      });
      return new SVGRenderer(); // 极限降级

    case 'spatial':
      if (capabilities.includes('realitykit')) return new RealityKitRenderer();
      if (capabilities.includes('arkit')) return new ARKitWebGLRenderer();
      return new WebGL360Renderer(); // VR视频降级

    default:
      throw new Error(`Unsupported platform: ${platform}`);
  }
}

// 特性降级策略
function adaptDescriptor(descriptor: Descriptor, platform: Platform): Descriptor {
  const overrides = platform.descriptor_override;

  return {
    ...descriptor,
    elements: descriptor.elements.map(el => {
      const override = overrides.color_mapping?.[el.color];
      return override ? { ...el, color: override } : el;
    }),
    animation: {
      enabled: overrides.animation?.enabled ?? true
    },
    interaction: {
      enabled: overrides.interaction?.enabled ?? true
    }
  };
}
```

---

## JSON格式示例

BCPP也支持JSON格式，便于程序处理：

```json
{
  "version": "1.0.0",
  "protocol": "browser-canvas-poetry/bcpp-1.0",
  "source": {
    "type": "poem",
    "text": "落霞与孤鹜齐飞，秋水共长天一色",
    "language": "zh-classical",
    "author": "王勃"
  },
  "intention": {
    "concept": {
      "primary": "自然与人文的和谐共生"
    },
    "style": {
      "primary": "shuimohua"
    },
    "mood": {
      "keywords": ["壮丽", "孤独", "宁静"]
    }
  },
  "agents": {
    "ink_wash": {
      "role": "atmospheric",
      "output_type": "atmosphere_map"
    },
    "pigment": {
      "role": "interactive",
      "output_type": "composition_tree"
    }
  },
  "descriptor": {
    "visual": {
      "background": {
        "type": "gradient",
        "stops": [
          {"position": 0, "color": "#2a1f4e"},
          {"position": 0.6, "color": "#c44569"},
          {"position": 1, "color": "#1a1a2e"}
        ]
      },
      "elements": [
        {
          "id": "sky",
          "type": "gradient",
          "z_index": 0
        },
        {
          "id": "duck",
          "type": "silhouette",
          "z_index": 1,
          "animation": {
            "path": "arc",
            "duration": 12000
          }
        }
      ]
    },
    "interaction": {
      "mappings": [
        {
          "trigger": "click",
          "target": "water",
          "effect": "ripple"
        }
      ]
    }
  },
  "render": {
    "targets": [
      {
        "id": "browser_canvas",
        "engine": "canvas_2d",
        "config": {
          "fps": 30
        }
      }
    ]
  },
  "validation": {
    "min_score": 0.75,
    "criteria": [
      {
        "id": "rhythm_presence",
        "weight": 0.3
      }
    ]
  }
}
```

---

## 使用指南

### 快速开始

1. **选择示例**：从上面选择一个最接近您需求的示例
2. **修改内容**：根据您的具体需求修改manifest.yaml
3. **验证格式**：使用BCPP验证器检查格式
4. **生成代码**：使用BCPP渲染器生成代码

### 格式转换

```javascript
// YAML → JSON
import yaml from 'js-yaml';
const jsonManifest = yaml.load(yamlString);

// JSON → YAML
import yaml from 'js-yaml';
const yamlManifest = yaml.dump(jsonObject);
```

### 验证清单

- [ ] 版本号正确
- [ ] 协议标识正确
- [ ] 所有必填字段存在
- [ ] 颜色值格式正确
- [ ] 动画时间合理
- [ ] 交互映射完整
- [ ] 验证标准设置

---

*BCPP Protocol Examples - 浏览器画布诗意协议示例集*
*让协议变得可触及、可复制、可创造*