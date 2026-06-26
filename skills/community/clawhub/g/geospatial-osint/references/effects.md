# Post-Processing Effects

## Cesium Post-Process Stages

### Built-in Effects

```javascript
// Bloom (glow)
const bloom = viewer.scene.postProcessStages.bloom;
bloom.enabled = true;
bloom.threshold = 0.8;
bloom.strength = 0.3;
bloom.radius = 0.5;

// FXAA (anti-aliasing)
viewer.scene.postProcessStages.fxaa.enabled = true;
```

### Custom Effects

```javascript
// CRT Effect
const crt = new Cesium.PostProcessStage({
  name: 'crt',
  uniforms: {
    scanlineIntensity: 0.15,
    scanlineCount: 800.0,
    vignetteStrength: 0.3,
    distortion: 0.02
  },
  fragmentShader: `
    uniform float scanlineIntensity;
    uniform float scanlineCount;
    uniform float vignetteStrength;
    uniform float distortion;
    
    varying vec2 v_textureCoord;
    uniform sampler2D colorTexture;
    
    void main() {
      vec2 uv = v_textureCoord;
      
      // Barrel distortion
      vec2 dc = uv - 0.5;
      float r2 = dot(dc, dc);
      uv += dc * r2 * distortion;
      
      vec4 color = texture2D(colorTexture, uv);
      
      // Scanlines
      float scanline = sin(uv.y * scanlineCount) * 0.5 + 0.5;
      color.rgb *= 1.0 - (scanlineIntensity * (1.0 - scanline));
      
      // Vignette
      float vignette = 1.0 - r2 * vignetteStrength * 4.0;
      color.rgb *= vignette;
      
      gl_FragColor = color;
    }
  `
});
viewer.scene.postProcessStages.add(crt);
```

## Night Vision (NVG)

```javascript
// NVG Green tint
const nvg = new Cesium.PostProcessStage({
  name: 'nvg',
  uniforms: {
    intensity: 1.0,
    noise: 0.05
  },
  fragmentShader: `
    uniform float intensity;
    uniform float noise;
    varying vec2 v_textureCoord;
    uniform sampler2D colorTexture;
    
    float rand(vec2 co) {
      return fract(sin(dot(co.xy, vec2(12.9898,78.233))) * 43758.5453);
    }
    
    void main() {
      vec4 color = texture2D(colorTexture, v_textureCoord);
      
      // Green channel dominant
      float luma = dot(color.rgb, vec3(0.299, 0.587, 0.114));
      vec3 nvg = vec3(0.0, luma * intensity, 0.0);
      
      // Add noise
      nvg += (rand(v_textureCoord) - 0.5) * noise;
      
      gl_FragColor = vec4(nvg, color.a);
    }
  `
});
```

## Thermal / FLIR

```javascript
// Thermal color mapping (inferno palette)
const thermal = new Cesium.PostProcessStage({
  name: 'thermal',
  fragmentShader: `
    varying vec2 v_textureCoord;
    uniform sampler2D colorTexture;
    
    vec3 inferno(float t) {
      // Simplified inferno colormap
      vec3 c0 = vec3(0.0, 0.0, 0.0);    // Black
      vec3 c1 = vec3(0.1, 0.0, 0.2);    // Dark purple
      vec3 c2 = vec3(0.4, 0.0, 0.3);    // Red-purple
      vec3 c3 = vec3(0.7, 0.2, 0.0);    // Orange
      vec3 c4 = vec3(1.0, 0.8, 0.2);    // Yellow
      vec3 c5 = vec3(1.0, 1.0, 0.9);    // White
      
      if (t < 0.2) return mix(c0, c1, t / 0.2);
      if (t < 0.4) return mix(c1, c2, (t - 0.2) / 0.2);
      if (t < 0.6) return mix(c2, c3, (t - 0.4) / 0.2);
      if (t < 0.8) return mix(c3, c4, (t - 0.6) / 0.2);
      return mix(c4, c5, (t - 0.8) / 0.2);
    }
    
    void main() {
      vec4 color = texture2D(colorTexture, v_textureCoord);
      float temp = dot(color.rgb, vec3(0.299, 0.587, 0.114));
      gl_FragColor = vec4(inferno(temp), color.a);
    }
  `
});
```

## Combining Effects

```javascript
// Effect chain
const effects = new Cesium.PostProcessStageComposite({
  stages: [crt, bloom, nvg],
  inputStages: [bloom, crt] // Order matters
});
```

## Quick Toggle

```javascript
function setVisualMode(mode) {
  const stages = viewer.scene.postProcessStages;
  
  // Disable all custom
  stages.removeAll();
  
  switch(mode) {
    case 'crt': stages.add(crt); break;
    case 'nv g': stages.add(nvg); break;
    case 'thermal': stages.add(thermal); break;
    case 'fluor': stages.add(fluor); break;
  }
}
```
