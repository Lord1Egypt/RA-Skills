# Satellite Pass Prediction

## Quick Method: n2yo.com

1. Go to https://www.n2yo.com/passes/
2. Enter your lat/lon
3. Select satellite NORAD ID

**Common satellites:**
- 25338: NOAA 19 (weather)
- 28654: Suomi NPP
- 27424: Terra (NASA)
- 37812: WorldView-2
- 27937: ISS

## Programmatic: Skyfield + TLE

```python
from skyfield.api import load, wgs84
from datetime import datetime, timedelta

# Load orbital data
ephemeris = load('de421.bsp')
satellites = load.tle_file('https://celestrak.org/NORAD/elements/gp.php?GROUP=visual&FORMAT=tle')

# Find ISS
iss = {sat.name: sat for sat in satellites}['ISS (ZARYA)']

# Your location
bluffton = wgs84.latlon(40.0383, -75.5977)

# Calculate passes
ts = load.timescale()
t = ts.now()

for i in range(5):
    t += 1  # advance 1 minute
    difference = iss - bluffton
    topocentric = difference(t)
    alt, az, distance = topocentric.altaz()

    if alt.degrees > 10:  # Above horizon
        print(f"{t.utc_datetime()}: {alt.degrees:.1f}° {az.degrees:.1f}°")
```

## TLE Sources

| Source | URL |
|--------|-----|
| CelesTrak (visual) | https://celestrak.org/NORAD/elements/gp.php?GROUP=visual&FORMAT=tle |
| CelesTrak (amateur) | https://celestrak.org/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle |
| CelesTrak (earth observation) | https://celestrak.org/NORAD/elements/gp.php?GROUP=earth-observation&FORMAT=tle |
| Space-Track (requires login) | https://www.space-track.org/ |

## Commercial Satellite Providers

| Provider | API | Cost |
|----------|-----|------|
| Planet Labs | https://api.planet.com/ | Pay-per-scene |
| Maxar | https://developer.maxar.com/ | Enterprise |
| Capella | https://www.capellaspace.com/ | Pay-per-scene |
| Airbus | https://www.airbus.com/ | Contact sales |

## Pass Prediction Tips

- **Dusk/dawn** = best visual satellite viewing (solar illumination)
- **Noon** = brightest for imagery
- **Radar (SAR)** works day/night, through clouds
- Check **elevation** — passes above 30° are most useful
