---
name: ci-cadastre-vertices
description: Find or verify parcel vertex coordinates on the Cote d'Ivoire Mining Cadastre Map Portal/Landfolio site. Use when a user gives an official parcel or license code and asks for vertices, boundary coordinates, WGS84/DMS coordinates, decimal latitude/longitude, Esri geometry, or a repeatable workflow on https://portals.landfolio.com/CoteDIvoire/en/.
---

# CI Cadastre Vertices

## Overview

Use live portal data. Parcel status, geometry, and even existence can change, so do not treat previously observed permits as stable examples. Prefer the official Esri geometry exposed by the loaded Landfolio page; use visual reconstruction only when page-state geometry is unavailable.

## Agent-Agnostic Workflow

Use whatever browser-control surface the current agent has: Playwright, Chrome DevTools, an in-app browser, OpenClaw-style browser control, Computer Use, or equivalent. The needed capabilities are: navigate, fill/search, wait for visible text, evaluate JavaScript in the page, and optionally inspect network requests.

1. Open `https://portals.landfolio.com/CoteDIvoire/en/`.
2. Dismiss the welcome panel if it appears.
3. Fill the field labeled `Search: Licenses, Parties` with the parcel/license code and submit.
4. Wait until the result panel contains the exact code. Record visible metadata such as group, code, status, party, type, and area. If multiple partial matches appear, select the exact `attributes.Code`.
5. Evaluate `window.Map.c_objCurrentSearchResults` in the page. Do not stringify whole Esri objects because they contain circular DOM/graphics references. Extract only:

```js
Object.fromEntries(
  Object.entries(window.Map.c_objCurrentSearchResults || {}).map(([group, items]) => [
    group,
    items.map((item) => ({
      layerId: item.layerId,
      mapServiceName: item.MapServiceName,
      attributes: item.feature && item.feature.attributes,
      geometryType: item.feature && item.feature.geometry && item.feature.geometry.type,
      rings: item.feature && item.feature.geometry && item.feature.geometry.rings,
      spatialReference: item.feature && item.feature.geometry && item.feature.geometry.spatialReference
    }))
  ])
)
```

6. Prefer an exact `attributes.Code` match. For active licences, the portal uses the `Permis Dynamic` service, whose configured REST URL is `https://mines.gouv.ci.cadastreminier.org/arcgis/rest/services/MapPortal/ActiveLicences/MapServer`. Direct service calls may return `499 Token Required`; the browser path is reliable because the app uses its own proxy/token flow.
7. Geometry usually arrives as Web Mercator rings in `wkid: 102100` / `latestWkid: 3857`. Drop the final duplicated closing point before reporting vertices.
8. Convert Web Mercator `(x, y)` to WGS84:

```js
const R = 6378137;
const lon = x / R * 180 / Math.PI;
const lat = (2 * Math.atan(Math.exp(y / R)) - Math.PI / 2) * 180 / Math.PI;
```

Cross-check in the page, when available:

```js
esri.geometry.webMercatorToGeographic(
  new esri.geometry.Point(x, y, Map.c_objMap.spatialReference)
)
```

9. Convert decimal degrees to DMS if requested: `degrees + minutes / 60 + seconds / 3600`; use `N` for positive latitude, `S` for negative latitude, `E` for positive longitude, and `W` for negative longitude.

## Visual Fallback

Use this only when the in-page result object or service geometry is unavailable.

1. Zoom and pan until the parcel polygon is large enough to inspect. Use stable map controls such as `Zoom In`, not fixed coordinates.
2. Open `Define Area of Interest`; the coordinate entry panel appears as `Saisir Coordonnees`.
3. Keep `WGS 1984` and `DMS`.
4. Use the live cursor coordinate readout only as a guide. Record saved coordinate rows from the panel as evidence.
5. Enter each vertex row as latitude degrees, minutes, seconds, `N`, longitude degrees, minutes, seconds, `W`. Use the plus-sign row for the next vertex.
6. Confirm the AOI overlays the parcel boundary and that the area is plausible.

## Drift And Evidence

- Do not embed or rely on fixed permit examples as truth. Permits may be renewed, revoked, reshaped, archived, or removed.
- Treat any prior successful permit lookup as a smoke test only after re-querying the live portal in the current run.
- Keep output tied to current evidence: visible portal result details plus extracted geometry source.
- If the browser cannot evaluate page JavaScript, inspect network responses for ArcGIS `query` calls or fall back to visual reconstruction.

## Output

Report the parcel code, portal result details, coordinate source, coordinate system, coordinate format, and vertices. Include both DMS and decimal degrees unless the user asks for only one format.

State whether the answer came from official in-page Esri geometry, direct service geometry, or visual reconstruction. Do not overstate visually reconstructed coordinates as surveyed boundary data.
