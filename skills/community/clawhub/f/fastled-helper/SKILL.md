---
name: fastled-helper
description: Use FastLED library for ESP32/Arduino LED strip control. Covers setup, color management (CRGB/CHSV), animations, palettes, power management, and chipset-specific configurations. Triggers on phrases like "FastLED", "LED strip", "WS2812", "NeoPixel", "APA102", "LED animation", "RGB LED", "addressable LED".
---

# FastLED Skill

FastLED is a high-performance library for controlling addressable RGB LED strips (WS2812/NeoPixel, APA102/DotStar, LPD8806, etc.) on ESP32, Arduino, and other platforms.

## Core Setup

### Include and LED Array
```cpp
#include "FastLED.h"

#define NUM_LEDS 60
#define DATA_PIN 6
#define CLOCK_PIN 7  // For SPI chipsets only

CRGB leds[NUM_LEDS];  // RGB color array, one per LED
```

### Initialize LED Strip (setup())

**3-wire chipsets** (WS2812, NeoPixel, etc.):
```cpp
void setup() {
    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
    // or: FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS);
}
```

**4-wire SPI chipsets** (APA102, LPD8806, etc.):
```cpp
void setup() {
    // Using hardware SPI pins
    FastLED.addLeds<APA102>(leds, NUM_LEDS);
    
    // Or with custom pins
    FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN>(leds, NUM_LEDS);
    
    // With custom data rate
    FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, RGB, DATA_RATE_MHZ(12)>(leds, NUM_LEDS);
}
```

### Show LEDs
```cpp
void loop() {
    leds[0] = CRGB::Red;   // Set first LED to red
    FastLED.show();         // Push data to strip
    delay(30);              // Wait before next frame
}
```

## Color Management

### CRGB - RGB Color Space

**Creating colors:**
```cpp
// Individual channels
leds[i].r = 255; leds[i].g = 128; leds[i].b = 0;

// Constructor
leds[i] = CRGB(255, 128, 0);

// Hex code
leds[i] = 0xFF8000;

// Named web colors
leds[i] = CRGB::HotPink;
leds[i] = CRGB::DarkOrange;

// setRGB method
leds[i].setRGB(255, 128, 0);
```

**Common predefined colors:**
```
CRGB::Black, CRGB::White, CRGB::Red, CRGB::Green, CRGB::Blue,
CRGB::Yellow, CRGB::Cyan, CRGB::Magenta, CRGB::Orange, CRGB::Purple
```

**CRGB methods:**
```cpp
leds[i].fadeToBlackBy(64);      // Fade by 64/256 (25%)
leds[i].fadeLightBy(64);        // Darken by 64/256
leds[i].nscale8_video(200);     // Scale to 78% brightness (video scaling)
leds[i].nscale8(200);           // Scale to 78% brightness (linear)
leds[i].maximizeBrightness();   // Maximize brightness (keep hue)
leds[i].invert();               // Invert color
```

### CHSV - HSV Color Space

FastLED uses 0-255 range for all HSV values (not 0-360/0-100):
```cpp
// Hue (0-255), Saturation (0-255), Value/Brightness (0-255)
leds[i] = CHSV(160, 255, 255);  // Full brightness blue

// Using named hue constants
leds[i] = CHSV(HUE_RED, 255, 255);
leds[i] = CHSV(HUE_GREEN, 200, 255);
leds[i] = CHSV(HUE_AQUA + 10, 255, 200);

// setHSV method
leds[i].setHSV(160, 255, 255);
```

**Hue cardinal points:**
```
HUE_RED (0), HUE_ORANGE (32), HUE_YELLOW (64), HUE_GREEN (96),
HUE_AQUA (128), HUE_BLUE (160), HUE_PURPLE (192), HUE_PINK (224)
```

**Color conversion:**
```cpp
CHSV hsvColor(160, 255, 255);
CRGB rgbColor = hsvColor;  // Automatic conversion
```

## LED Control Functions

### Fill Functions
```cpp
// Fill all LEDs with solid color
fill_solid(leds, NUM_LEDS, CRGB::Red);

// Fill range with solid color
fill_solid(&(leds[10]), 20, CRGB::Blue);

// Fill with gradient (start color to end color)
fill_gradient_RGB(leds, NUM_LEDS, CRGB::Red, CRGB::Blue);

// Fill with HSV gradient
fill_gradient(leds, NUM_LEDS, CHSV(0, 255, 255), CHSV(160, 255, 255));

// Fill with HSV gradient (3-color)
fill_gradient(leds, 0, CHSV(0,255,255), NUM_LEDS/2, CHSV(100,255,255), 
              NUM_LEDS-1, CHSV(200,255,255), SHORTEST_HUES);

// Fill rainbow
fill_rainbow(leds, NUM_LEDS, 0, 5);  // Start hue 0, delta 5 per LED
```

### Copy/Move Functions
```cpp
// Copy single LED
leds[i] = leds[j];

// Copy range
memmove(&leds[dest], &leds[src], 10 * sizeof(CRGB));
memmove8(&leds[dest], &leds[src], 10 * sizeof(CRGB));  // Faster on AVR

// Shift LEDs (move all one position)
memmove(&leds[1], &leds[0], (NUM_LEDS-1) * sizeof(CRGB));
leds[0] = CRGB::Black;  // Clear first

// Fade all to black
fadeToBlackBy(leds, NUM_LEDS, 64);  // Fade by 64/256

// Dim all
nscale8(leds, NUM_LEDS, 200);  // Scale to 78%
```

### Brightness and Power
```cpp
// Set global brightness (0-255)
FastLED.setBrightness(128);  // 50% brightness

// Get current power usage (in milliwatts)
uint16_t milliwatts = calculate_unscaled_power_mW(leds, NUM_LEDS);

// Limit power usage
FastLED.setMaxPowerInVoltsAndMilliamps(5, 1500);  // 5V, 1.5A max
```

## Color Palettes

### Built-in Palettes
```cpp
// Use built-in palette
CRGBPalette16 myPal = RainbowColors_p;
CRGBPalette16 myPal = RainbowStripeColors_p;
CRGBPalette16 myPal = OceanColors_p;
CRGBPalette16 myPal = CloudColors_p;
CRGBPalette16 myPal = LavaColors_p;
CRGBPalette16 myPal = ForestColors_p;
CRGBPalette16 myPal = PartyColors_p;
CRGBPalette16 myPal = HeatColors_p;
```

### Custom Gradient Palettes
```cpp
// Define gradient palette (stored in PROGMEM)
DEFINE_GRADIENT_PALETTE( heatmap_gp ) {
    0,     0,  0,  0,   // black
  128,   255,  0,  0,   // red
  224,   255,255,  0,   // bright yellow
  255,   255,255,255 }; // full white

// Activate
CRGBPalette16 myPal = heatmap_gp;

// Use
uint8_t index = 128;  // 0-255
leds[i] = ColorFromPalette(myPal, index);
leds[i] = ColorFromPalette(myPal, index, 128);  // With brightness 128
leds[i] = ColorFromPalette(myPal, index, 255, NOBLEND);  // No blending
```

### Palette Blending
```cpp
CRGBPalette16 currentPalette;
CRGBPalette16 targetPalette;
uint8_t paletteBlendAmount = 0;

// Blend between palettes
nblendPaletteTowardPalette(currentPalette, targetPalette, 24);
```

## Animation Helpers

### Linear Blending
```cpp
// Blend between two colors
CRGB colorA = CRGB::Red;
CRGB colorB = CRGB::Blue;
leds[i] = blend(colorA, colorB, 128);  // 50% blend

// Blend with black (fade)
leds[i] = blend(leds[i], CRGB::Black, 64);
```

### Beat Functions (Time-based Animation)
```cpp
// Returns 0-255 based on BPM
uint8_t beat = beatsin8(60);  // 60 BPM sine wave

// With low/high range
uint8_t beat = beatsin8(60, 20, 200);  // Range 20-200

// With phase offset
uint8_t beat = beatsin8(60, 20, 200, 0, 64);  // Phase offset 64

// Other beat functions
uint16_t beat16 = beatsin16(60);        // 16-bit precision
uint8_t beat88 = beatsin88(60 << 8);     // 8.8 fixed point
```

### Wave Functions
```cpp
// Triwave (triangle wave)
uint8_t val = triwave8(128);  // 0-255 range

// Quadwave (smoother)
uint8_t val = quadwave8(128);

// Cubic wave (even smoother)
uint8_t val = cubicwave8(128);

// Sine wave
uint8_t val = sin8(128);      // 0-255 range (half wave)
uint8_t val = cos8(128);      // 0-255 range (half wave)
```

### Random Functions
```cpp
// Random 8-bit value
uint8_t r = random8();
uint8_t r = random8(100);     // 0-99

// Random 16-bit value
uint16_t r = random16();

// Random CRGB color
CRGB c = CRGB(random8(), random8(), random8());
```

## Multi-Strip and Parallel Output

### Multiple LED Arrays
```cpp
#define NUM_LEDS_STRIP_A 60
#define NUM_LEDS_STRIP_B 30

#define DATA_PIN_A 6
#define DATA_PIN_B 7

CRGB ledsA[NUM_LEDS_STRIP_A];
CRGB ledsB[NUM_LEDS_STRIP_B];

void setup() {
    FastLED.addLeds<NEOPIXEL, DATA_PIN_A>(ledsA, NUM_LEDS_STRIP_A);
    FastLED.addLeds<NEOPIXEL, DATA_PIN_B>(ledsB, NUM_LEDS_STRIP_B);
}

void loop() {
    fill_solid(ledsA, NUM_LEDS_STRIP_A, CRGB::Red);
    fill_solid(ledsB, NUM_LEDS_STRIP_B, CRGB::Blue);
    FastLED.show();
}
```

### Parallel Output (Teensy/ESP32)
```cpp
// ESP32: Up to 8 parallel strips
#define NUM_STRIPS 8
#define NUM_LEDS_PER_STRIP 60

CRGB leds[NUM_STRIPS * NUM_LEDS_PER_STRIP];

void setup() {
    FastLED.addLeds<WS2812, 2, GRB>(leds, 0, NUM_LEDS_PER_STRIP);
    FastLED.addLeds<WS2812, 3, GRB>(leds, 1 * NUM_LEDS_PER_STRIP, NUM_LEDS_PER_STRIP);
    FastLED.addLeds<WS2812, 4, GRB>(leds, 2 * NUM_LEDS_PER_STRIP, NUM_LEDS_PER_STRIP);
    // ... up to 8 strips
}
```

## Supported Chipsets

### 3-Wire (Data only)
| Chipset | Alias | Data Rate | Notes |
|---------|-------|-----------|-------|
| WS2811 | | 800kbps | |
| WS2812 | NEOPIXEL | 800kbps | LED+controller in one package |
| WS2812B | NEOPIXEL | 800kbps | Most common |
| WS2813 | | 800kbps | Backup data line |
| SK6812 | | 800kbps | RGBW support |
| TM1809 | | 800kbps | 1 IC per 3 LEDs |
| TM1804 | | 800kbps | 1 IC per 1 LED |
| TM1803 | | 400kbps | RadioShack version |
| UCS1903 | | 400kbps | Very slow |
| UCS1904 | | 800kbps | |
| UCS2903 | | 800kbps | |

### 4-Wire SPI (Data + Clock)
| Chipset | Alias | Data Rate | Notes |
|---------|-------|-----------|-------|
| APA102 | DOTSTAR | ~24Mbps | Recommended |
| SK9822 | | ~24Mbps | APA102 clone |
| LPD8806 | | 1-20Mbps | 7-bit per channel |
| WS2801 | | 1Mbps | Older, glitch-prone |
| P9813 | TCL | 1-15Mbps | Total Control Lighting |
| SM16716 | | | Poor protocol |

### Color Order Specifiers
```cpp
RGB, RBG, GRB, GBR, BRG, BGR  // Common for 3-wire
RBG, BGR, etc.                  // For RGBW (add W at end)
```

## ESP32-Specific Notes

### GPIO Pins
- Any GPIO can be used for data output
- Recommended: GPIO 2, 4, 12-19, 21-23, 25-27, 32-33
- Avoid: GPIO 6-11 (used for flash), GPIO 34-39 (input only)

### RMT Peripheral (Hardware Assist)
```cpp
// FastLED on ESP32 uses RMT peripheral for precise timing
// No interrupt disabling needed (unlike AVR)

// Increase RMT channels if needed (default is usually sufficient)
#define FASTLED_RMT_MAX_CHANNELS 8
```

### Power Considerations
- ESP32 3.3V GPIO can drive 5V LED strips directly (usually works)
- For long strips, use level shifter (3.3V → 5V)
- Power LED strip separately from ESP32 (don't power 5V strip from ESP32)

## Common Patterns

### Rainbow Cycle
```cpp
uint8_t hue = 0;

void loop() {
    fill_rainbow(leds, NUM_LEDS, hue, 255 / NUM_LEDS);
    FastLED.show();
    hue++;
    delay(20);
}
```

### Color Wipe
```cpp
void colorWipe(CRGB color, int wait) {
    for(int i=0; i<NUM_LEDS; i++) {
        leds[i] = color;
        FastLED.show();
        delay(wait);
    }
}
```

### Running Dot
```cpp
void loop() {
    fadeToBlackBy(leds, NUM_LEDS, 64);
    int pos = beatsin16(60, 0, NUM_LEDS-1);
    leds[pos] = CHSV(hue, 255, 255);
    FastLED.show();
}
```

### Fire Effect
```cpp
void fireEffect() {
    CRGBPalette16 heatPalette = HeatColors_p;
    for(int i=0; i<NUM_LEDS; i++) {
        uint8_t noise = inoise8(i * 50, millis() / 10);
        uint8_t index = scale8(noise, 240);
        leds[i] = ColorFromPalette(heatPalette, index);
    }
    FastLED.show();
}
```

## Tips and Gotchas

- **show() is blocking** on most platforms (sends all data before returning)
- **WS2812 requires precise timing** - interrupts disabled during send on AVR, but not ESP32
- **Power supply**: Budget 60mA per LED at full white. 300 LEDs = 18A max
- **Capacitor**: Add 1000μF across power supply near strip start
- **Resistor**: Add 330-470Ω in series on data line near strip start
- **Level shifter**: Use for 5V strips with 3.3V MCU if data glitches
- **Memory**: Each CRGB is 3 bytes. 1000 LEDs = 3KB RAM
- ** Temporal dithering**: Improves low-brightness smoothness, enabled by default
- **Color correction**: `FastLED.setCorrection(TypicalLEDStrip)` or `UncorrectedColor`
- **Temperature**: `FastLED.setTemperature(ClearBlueSky)` or `Tungsten40W`

## Resources

- Official docs: http://fastled.io/docs
- GitHub: https://github.com/FastLED/FastLED
- Wiki: https://github.com/FastLED/FastLED/wiki
- Demos: https://github.com/FastLED/FastLED/tree/master/examples
