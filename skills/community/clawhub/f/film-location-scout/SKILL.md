---
name: film-location-scout
version: 1.0.0
description: >-
  Discover nearby film and TV show shooting locations based on the user's current city and position.
  Outputs 5 self-contained cases, each with a cinematic scene recreation image featuring 1-2 prominent characters/people
  in the foreground (perfect for photo recreation), precise GPS coordinates, scene description, and weather-based photography parameters.
  Use when the user mentions film locations, movie shooting spots, TV drama filming sites,
  cinematic photography, scene pilgrimage, or wants to find nearby places where movies were filmed.
  Also trigger when user asks about photography at famous film locations or wants a film-inspired
  photo guide.
author: Qoder
license: MIT
tags:
  - film
  - location
  - photography
  - travel
  - cinema
  - movie
  - scene
  - tourism
---

# Film Location Scout

Discover 5 nearby film/TV shooting locations. Each case is self-contained: cinematic scene image with 1-2 prominent characters in the foreground (perfect for photo recreation) + precise location + photography parameters.

## Trigger

User invokes `/film-location-scout` or asks naturally:
- "帮我找附近的电影取景地"
- "推荐一些可以拍照的电影场景地点"
- "附近有什么电影拍摄地"
- "film locations near me"
- "movie shooting spots nearby"

## Workflow

```
Step 1: Get User Location (IP + confirm)
        |
Step 2: Get Weather & Light Conditions
        |
Step 3: Find 5 Filming Locations within 5km (each as a complete case)
        |
        For each of the 5 cases:
          3a. Location + precise coordinates
          3b. Film scene description
          3c. Per-location photography parameters
          3d. Generate cinematic scene image (with 1-2 prominent characters in foreground)
        |
Step 4: Output all 5 cases
```

## Step 1: Get User Location

**Phase A - IP auto-detect:**

Use WebFetch to query: `https://ipinfo.io/json`

Extract: `city`, `region`, `country`, `loc` (lat,lon).

**Phase B - User confirmation:**

Use AskUserQuestion:
> "Detected you are in **{city}**. Is that correct? Please also provide your specific location (landmark, intersection, or address) for precise nearby search."

Store:
- `city_name`: city name (Chinese + English)
- `user_lat`, `user_lon`: **6 decimal places** precision (e.g., `31.230416, 121.473701`)

## Step 2: Get Weather & Light Conditions

Use WebSearch: `"{city_name}" weather now temperature humidity`

Record:
- `weather`: condition (sunny/cloudy/rainy/foggy/snowy/night)
- `temperature`: current temp
- `humidity`, `wind`, `visibility`
- `time_of_day`: calculate from current local time -> golden hour / blue hour / midday / overcast / night
- `sun_position`: high / low / setting / rising

These will be used per-case in Step 3c.

## Step 3: Build 5 Cases

Search for filming locations near the user using built-in knowledge + WebSearch:

1. WebSearch queries (run multiple):
   - `"{city_name}" famous movie filming locations exact address`
   - `"{city_name}" TV drama shooting spots GPS coordinates`
   - `"{city_name}" film scenes famous landmarks`
   - Also search in Chinese: `"{city_name}" 电影取景地 地址`
2. From results, select **exactly 5** locations that:
   - Are within **5km** of user (expand to 10km if <5 found, note this)
   - Come from well-known, diverse films/shows (mix genres, eras)
   - Have identifiable, visitable spots
3. For each location, use WebSearch to get **precise coordinates**:
   - Query: `"{location_name}" GPS coordinates` or `"{location_name}" 经纬度`
   - Coordinates MUST be **6 decimal places** (e.g., `31.239728, 121.499718`)
   - If WebSearch cannot provide exact coordinates, search for the venue/landmark coordinates directly

### For EACH of the 5 cases, produce all 4 parts:

#### 3a. Precise Location Info

```
Name:        {location_name} ({location_name_english})
Address:     {full_street_address, including district}
Coordinates: {lat_6dp}, {lon_6dp}
Distance:    {distance_in_meters}m from your position
Map:         https://www.google.com/maps?q={lat},{lon}
```

- Address must include district/neighborhood level detail
- Distance in **meters** (not km) for locations <1km; in km with 1 decimal for >1km

#### 3b. Film Scene Description

```
Film:     {title} ({original_title}, {year})
Director: {director}
Genre:    {genre}
Scene:    {detailed_description_of_the_specific_scene}
```

The scene description must be **concrete and vivid** (3-5 sentences):
- What happens in the scene (plot context)
- What the shot looks like (camera angle, framing, movement)
- What makes this location recognizable in the film
- Timestamp or episode reference if available (e.g., "01:23:45" or "S02E05")

#### 3c. Photography Parameters (per-location)

Read [photo-params-reference.md](photo-params-reference.md) for the parameter matrix.

Combine the weather/light from Step 2 with **this specific location's characteristics** to produce tailored settings:

```
Light Condition: {time_of_day} + {weather} at {location_type}

Camera Settings:
  Aperture:      f/{value}  ({reason_for_this_location})
  Shutter Speed: {value}    ({reason})
  ISO:           {value}    ({reason})
  White Balance: {value}K   ({reason})
  Exposure Comp: {value} EV ({reason})
  Focal Length:  {value}mm  ({reason_matching_film_shot})

Composition Tip: {1-2 sentences on how to frame THIS specific location to match the film}
Phone Tip:       {1 sentence for phone users}
```

Key: the focal length should **match the look of the original film shot** when possible. The composition tip must reference the specific film scene.

#### 3d. Generate Cinematic Scene Image

Use **ImageGen** for each case. Read [scene-prompts.md](scene-prompts.md) for prompt templates.

**CRITICAL REQUIREMENTS for the image:**

1. **1-2 prominent characters/people in the foreground** - This is ESSENTIAL for photo recreation
   - Characters should be clearly visible and take up significant frame space (not tiny background figures)
   - Position them in the foreground or middle ground where they can be the focus
   - Show their full body or 3/4 body, not just tiny silhouettes

2. **Realistic photographic style** - Must look like a real movie still / film screenshot:
   - Photorealistic, shot on 35mm film aesthetic
   - The **real landmark/venue** as recognizable background
   - Cinematic color grading matching the film's visual tone
   - Film-accurate camera angle and composition
   - Appropriate lighting reflecting the film's mood and current weather

3. **NOT illustration, NOT sketch, NOT cartoon**

Parameters:
- Size: `1024x768`
- Name: `scene-{case_number}-{location_slug}`

**IMPORTANT**: Generate **5 separate images**, one per case. Do NOT batch into a single image.

## Step 4: Output Format

Present as 5 self-contained cards. Each card has all 4 parts together:

```markdown
# {City} Film Location Scout

> Location: {user_location} | Time: {time} | Weather: {weather} {temp}

---

## Case 1: {location_name}

### Film
**{title}** ({year}) dir. {director}
{detailed_scene_description}

### Location
- Address: {full_address}
- Coordinates: `{lat_6dp}, {lon_6dp}`
- Distance: {distance} from you
- [Open in Maps](https://www.google.com/maps?q={lat},{lon})

### Photography Settings
| Parameter | Value | Reason |
|-----------|-------|--------|
| Aperture | f/{val} | {reason} |
| Shutter | {val} | {reason} |
| ISO | {val} | {reason} |
| WB | {val}K | {reason} |
| EV | {val} | {reason} |
| Focal | {val}mm | {reason} |

> Composition: {composition_tip}
> Phone: {phone_tip}

### Scene Image
{scene_image}

**Photo Recreation Tip**: Stand where the {character_description} is positioned in the image above. Frame yourself similarly with the {landmark_feature} visible in the background for the perfect recreation shot.

---

## Case 2: {location_name}
...

[Cases 3-5 follow same structure]
```

## Error Handling

- IP geolocation fails -> ask user directly
- <5 locations within 5km -> expand to 10km, note this
- No films for city -> broaden to province/region
- Weather unavailable -> use general outdoor params from reference
- ImageGen fails -> describe composition in text
- Coordinates imprecise -> use the landmark/venue's known coordinates, never round beyond 6 decimal places

## Logging

Throughout the execution, log key information for transparency and debugging:

### Log Structure

```
[LOG] {timestamp} | {step} | {status} | {details}
```

### Required Log Points

1. **Location Detection**
   - `[LOG] {time} | LOCATION | DETECTED | City: {city}, Coords: {lat},{lon}`
   - `[LOG] {time} | LOCATION | CONFIRMED | User confirmed: {confirmed_location}`

2. **Weather Fetch**
   - `[LOG] {time} | WEATHER | FETCHED | {weather}, {temp}°C, {condition}`
   - `[LOG] {time} | LIGHT | CALCULATED | {time_of_day}, {sun_position}`

3. **Location Search**
   - `[LOG] {time} | SEARCH | STARTED | Querying {city} film locations`
   - `[LOG] {time} | SEARCH | FOUND | {count} locations within {radius}km`
   - `[LOG] {time} | SELECTED | {location_name} | Film: {title} | Distance: {distance}m`

4. **Image Generation**
   - `[LOG] {time} | IMAGE | GENERATING | Case {n}: {location_name}`
   - `[LOG] {time} | IMAGE | SUCCESS | Case {n}: {filename} generated`
   - `[LOG] {time} | IMAGE | FAILED | Case {n}: {error_reason}`

5. **Completion**
   - `[LOG] {time} | COMPLETE | {total_cases} cases generated | Total distance range: {min}m - {max}m`

### Log Output

Present logs in a collapsible section at the end of the response:

```markdown
<details>
<summary>Execution Log</summary>

```
[LOG] 14:32:01 | LOCATION | DETECTED | City: Shanghai, Coords: 31.230416,121.473701
[LOG] 14:32:03 | LOCATION | CONFIRMED | User confirmed: The Bund
[LOG] 14:32:05 | WEATHER | FETCHED | Cloudy, 18°C, Overcast
...
```

</details>
```

## Skill Description

### Purpose
Film Location Scout helps users discover nearby film and TV shooting locations for cinematic photography and scene recreation. It combines real-world location data with film scene information to create a complete photo guide.

### Capabilities
- Auto-detects user location via IP geolocation
- Searches for film/TV shooting locations within 5km radius
- Generates cinematic scene images with prominent characters for photo reference
- Provides precise GPS coordinates and navigation links
- Calculates weather-based photography parameters
- Offers composition tips matching the original film shots

### Output Format
5 self-contained cases, each containing:
1. **Film Info**: Title, director, genre, detailed scene description
2. **Location**: Name, full address, precise coordinates (6 decimal places), distance, map link
3. **Photography Settings**: Aperture, shutter, ISO, WB, EV, focal length with reasons
4. **Scene Image**: AI-generated cinematic still with 1-2 prominent characters for photo recreation

### Use Cases
- **Photo Recreation**: Users can stand where characters stood and recreate iconic shots
- **Film Tourism**: Discover filming locations while traveling
- **Cinematic Photography**: Learn professional camera settings for location shooting
- **Scene Pilgrimage**: Visit famous movie spots in your own city

### Limitations
- Requires locations to be within database/knowledge coverage
- Image generation depends on AI capabilities and may not perfectly match the film
- Weather data is current conditions, not when the scene was filmed
- Coordinates accuracy depends on available data sources

### Dependencies
- IP geolocation service (ipinfo.io)
- Web search for location and weather data
- Image generation capability
- Real-time weather information
