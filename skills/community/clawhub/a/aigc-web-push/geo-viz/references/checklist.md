# Geographic shot checklist

In addition to host QA:

## Data / facts

- [ ] `geo/manifest.json` (or equivalent) with sources and license
- [ ] WGS84; vertical datum noted if elevation used
- [ ] Historical routes verified — not raw modern OSM
- [ ] Required attribution on screen

## Tech

- [ ] Motion from Remotion frame or HyperFrames seek only
- [ ] No blank / flash frames; assets ready before render
- [ ] HF: basemap is baked; no live tiles at render
- [ ] No Key/Token basemap as the default path
- [ ] Aspect ratio not hard-locked to one ratio

## Story

- [ ] Object → visible change → result (route grow, dive, cut, …)
- [ ] No AI fake satellite / terrain as the hero
- [ ] Not an info-card slideshow standing in for geography

## Global

- [ ] No per-country forks; swap bbox / data / locale only
- [ ] Labels follow `locale`
