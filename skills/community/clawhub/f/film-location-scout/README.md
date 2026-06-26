# Film Location Scout Skill

Discover nearby film and TV show shooting locations with cinematic scene recreation images. Perfect for photo recreation, film tourism, and cinematic photography.

## Features

- **Auto Location Detection**: Detects your city via IP geolocation
- **5 Curated Locations**: Finds 5 film/TV shooting spots within 5km of your position
- **Cinematic Scene Images**: AI-generated movie stills with 1-2 prominent characters for photo reference
- **Precise Coordinates**: GPS coordinates with 6 decimal places accuracy
- **Photography Parameters**: Weather-based camera settings (aperture, shutter, ISO, etc.)
- **Composition Tips**: Film-accurate framing advice for each location

## Installation

### Quick Install (Auto-detect)

```bash
./install.sh
```

### Install for Specific Platform

```bash
# Claude Code
./install.sh --platform claude

# Cursor (project-level)
./install.sh --platform cursor

# Cursor (user-level)
./install.sh --platform cursor --user

# GitHub Copilot
./install.sh --platform copilot

# Windsurf
./install.sh --platform windsurf

# All detected platforms
./install.sh --all
```

### Manual Install

```bash
# Clone to your platform's skill directory

# Claude Code
git clone <repo-url> ~/.claude/skills/film-location-scout

# Cursor
git clone <repo-url> .cursor/rules/film-location-scout

# GitHub Copilot
git clone <repo-url> .github/skills/film-location-scout

# Universal (works with most platforms)
git clone <repo-url> ~/.agents/skills/film-location-scout
```

## Usage

Once installed, invoke the skill with:

```
/film-location-scout
```

Or naturally:

```
帮我找附近的电影取景地
推荐一些可以拍照的电影场景地点
附近有什么电影拍摄地
film locations near me
movie shooting spots nearby
```

### Examples

**Basic search:**
```
/film-location-scout
```

**With specific city:**
```
/film-location-scout Find film locations in Paris
```

**Photo recreation focus:**
```
/film-location-scout I want to recreate movie scenes in Tokyo
```

## How It Works

The skill follows a 4-step workflow:

1. **Location Detection**: Auto-detects your city via IP, confirms with you
2. **Weather Fetch**: Gets current weather and light conditions
3. **Location Search**: Finds 5 filming locations within 5km radius
4. **Case Generation**: For each location, generates:
   - Precise location info (address, coordinates, map link)
   - Film scene description (plot, camera angles, timestamps)
   - Photography parameters (tailored to weather and location)
   - Cinematic scene image (with 1-2 prominent characters for photo reference)

## Output Format

Each of the 5 cases includes:

### Film Info
- Title, director, genre, year
- Detailed scene description (3-5 sentences)
- Camera angles, framing, movement
- Timestamp/episode reference

### Location
- Name (Chinese + English)
- Full street address with district
- Precise coordinates (6 decimal places)
- Distance from your position
- Google Maps link

### Photography Settings
| Parameter | Example | Purpose |
|-----------|---------|---------|
| Aperture | f/2.8 - f/16 | Depth of field control |
| Shutter | 1/60s - 1/1000s | Motion freeze/blur |
| ISO | 100 - 6400 | Light sensitivity |
| White Balance | 3000K - 7000K | Color temperature |
| Exposure Comp | -1.0 to +1.7 EV | Exposure adjustment |
| Focal Length | 24mm - 85mm | Field of view |

Plus composition tips and phone photography advice.

### Scene Image
AI-generated cinematic still featuring:
- 1-2 prominent characters in foreground (for photo recreation reference)
- Real landmark/venue as recognizable background
- Film-accurate color grading and lighting
- Photorealistic movie still aesthetic

## Project Structure

```
film-location-scout/
├── SKILL.md                    # Main skill definition
├── README.md                   # This file
├── install.sh                  # Cross-platform installer
├── .skill-metadata.yaml        # Skill metadata
├── scene-prompts.md            # Image generation prompt templates
├── photo-params-reference.md   # Photography parameter matrix
├── assets/                     # Static assets
└── scripts/                    # Utility scripts
    └── distance_calc.py        # Haversine distance calculator
```

## Reference Files

### scene-prompts.md
Detailed templates for generating cinematic scene images:
- Character prominence guidelines (20-40% of frame)
- Lighting descriptions for different weather conditions
- Color grading for various film styles
- Camera angle and lens recommendations
- Scene type templates (urban, waterfront, historic, park, interior)

### photo-params-reference.md
Photography parameter matrix:
- Light condition settings (golden hour, blue hour, midday, overcast, rainy, foggy, night, snow)
- Phone photography quick settings
- Film-specific composition tips

## Configuration

No configuration required. The skill auto-detects:
- Your location via IP geolocation
- Current weather conditions
- Local time for light calculations

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong city detected | Manually provide your location when prompted |
| < 5 locations found | Search radius auto-expands to 10km |
| Image generation fails | Scene described in text instead |
| Coordinates seem wrong | Verify with Google Maps link provided |
| Weather unavailable | Uses general outdoor photography parameters |

## Requirements

- Internet connection (for location, weather, and image generation)
- Image generation capability
- Web search capability

## Use Cases

### Photo Recreation
Stand where the character is positioned in the generated image. Frame yourself similarly with the landmark visible in the background for the perfect recreation shot.

### Film Tourism
Discover filming locations while traveling to new cities. Visit iconic movie spots and learn the behind-the-scenes stories.

### Cinematic Photography
Learn professional camera settings tailored to each location's lighting conditions and the original film's visual style.

### Scene Pilgrimage
Explore famous movie spots in your own city. See your hometown through the lens of cinema.

## Limitations

- Requires locations to be within database/knowledge coverage
- Image generation depends on AI capabilities and may not perfectly match the film
- Weather data reflects current conditions, not when the scene was originally filmed
- Coordinates accuracy depends on available data sources
- Some locations may be private property or have access restrictions

## Dependencies

- IP geolocation service (ipinfo.io)
- Web search for location and weather data
- Image generation capability
- Real-time weather information sources

## License

MIT License

## Contributing

Contributions welcome! Please ensure:
- Code follows existing style
- All scripts have proper error handling
- New features include documentation updates
- Test on multiple platforms before submitting

## Credits

- Film locations data sourced from public filming location databases
- Photography parameters based on professional cinematography guides
- Scene recreation inspired by film tourism community practices
