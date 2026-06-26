# Fingerprinting Detection Patterns

## Canvas Fingerprinting
**API calls to detect:**
- `HTMLCanvasElement.prototype.toDataURL`
- `CanvasRenderingContext2D.prototype.getImageData`
- Drawing text with specific fonts then reading pixel data
- Creating off-screen canvas elements

**Pattern:** Script creates a canvas, draws text/shapes, then calls `toDataURL()` or `getImageData()` to extract a hash unique to the device's GPU/rendering engine.

## WebGL Fingerprinting
**API calls to detect:**
- `WebGLRenderingContext.prototype.getParameter`
- `WEBGL_debug_renderer_info` extension access
- `getExtension('WEBGL_debug_renderer_info')`
- Reading `UNMASKED_VENDOR_WEBGL` or `UNMASKED_RENDERER_WEBGL`

**Pattern:** Script queries WebGL for GPU vendor/renderer strings and supported extensions to build a device profile.

## AudioContext Fingerprinting
**API calls to detect:**
- `AudioContext` or `webkitAudioContext` constructor
- `createOscillator()`
- `createAnalyser()`
- `createDynamicsCompressor()`
- `destination` access followed by `getFloatFrequencyData` or `getByteFrequencyData`

**Pattern:** Script creates an audio signal, processes it through compressor/analyser nodes, and reads the output — differences in audio processing reveal device characteristics.

## Font Fingerprinting
**API calls to detect:**
- Creating spans with specific font-family values and measuring offsetWidth/offsetHeight
- Using `document.fonts.check()` or `document.fonts.ready`
- Iterating through a large list of font names

**Pattern:** Script tests which fonts are installed by measuring rendered text dimensions with fallback detection.

## Navigator / Screen Fingerprinting
**Properties commonly harvested:**
- `navigator.userAgent`, `navigator.platform`, `navigator.language`
- `navigator.hardwareConcurrency`, `navigator.deviceMemory`
- `navigator.plugins`, `navigator.mimeTypes`
- `screen.width`, `screen.height`, `screen.colorDepth`
- `screen.availWidth`, `screen.availHeight`
- `window.devicePixelRatio`
- `Intl.DateTimeFormat().resolvedOptions().timeZone`

**Suspicious pattern:** Accessing 5+ of these properties in rapid succession, especially when combined with hashing.

## TLS / JA3 Fingerprinting
Not detectable from client-side JavaScript — happens at the network layer. Mention in report if relevant to the user's threat model.

## Known Fingerprinting Libraries
- FingerprintJS / @fingerprintjs/fingerprintjs
- ClientJS
- Evercookie
- Canvas-fingerprint
- AudioFP
