# Ascent methods and selection rationale

[简体中文](ascent-options.md) | [English](ascent-options.en.md)

**The default is no averaging with a 10 m peak/valley reversal threshold.** Across the twenty trail activities tested, this method was closest overall to Garmin's displayed totals and avoided further suppression of short hills by window averaging. Other windows remain explicit options.

## Historical method comparison

All methods used the same original FIT coordinates and elevations for twenty activities, compared against Garmin's displayed ascent and descent. Mean absolute difference is the average of the absolute differences for individual activities; platform totals are not terrain ground truth.

| Method | Mean absolute ascent difference (m) | Mean absolute descent difference (m) |
| --- | ---: | ---: |
| Legacy 100 m window | 110.5 | 111.3 |
| **No averaging + 10 m threshold (default)** | **71.4** | **71.9** |
| 40 m averaging + 10 m threshold | 105.9 | 107.0 |
| 20 m averaging + 10 m threshold | 88.6 | 89.7 |
| 10 m averaging + 10 m threshold | 79.1 | 79.9 |

Ascent for three race routes is shown below in metres. All five methods used the same input for each route and produced identical distances.

| Route | Legacy 100 m | No averaging + 10 m | 40 m + 10 m | 20 m + 10 m | 10 m + 10 m |
| --- | ---: | ---: | ---: | ---: | ---: |
| Huizhou Ancient City 100K | 5331.6 | 5965.5 | 5521.0 | 5768.6 | 5852.6 |
| Dajingmen DGW100K | 3635.0 | 3729.0 | 3575.0 | 3651.8 | 3680.8 |
| Dajingmen MGW50K | 1900.8 | 1960.0 | 1867.8 | 1929.3 | 1949.9 |

These are historical experiment snapshots: `28270dc` for legacy, `461ace7` for no averaging, and `dd4b95e` for the 40/20/10 m windows. They are not recalculated after every update. The current default remains no averaging + 10 m. Only aggregates from the twenty personal activities are published; without the raw FIT files, that set of statistics cannot be reproduced from the public repository alone.

The full repository now includes the MGW50K [original GPX](https://github.com/yihouzenmeban/trail-running-pace/blob/main/examples/大境门/DGW50K/2026京东大境门古长城越野赛by%20UTMB®MGW50K.gpx), [elevation-filled copy](https://github.com/yihouzenmeban/trail-running-pace/blob/main/examples/大境门/DGW50K/MGW50K-elevation-filled.gpx), and [repair report](https://github.com/yihouzenmeban/trail-running-pace/blob/main/examples/大境门/DGW50K/elevation-repair.json). All methods in the table used that same distance-interpolated copy, filling 59 missing elevations across gaps of approximately 835 m and 34 m. Missing terrain cannot be recovered. Public-route reproduction commands are in the example notes; independently installed Skills do not need these case files.

## Huizhou Ancient City before and after the race

### Pre-race GPX inspection

On the same pre-race GPX, no averaging adds approximately 634 m relative to legacy, with **77.9% of that difference between CP3 and CP6**. Inspection at that stage found no confirmed isolated large spikes to remove or elevation jumps at CP boundaries. Independent turning-point accumulation also returned 5965.47 m. This only ruled out the inspected anomaly types, not errors in continuous undulations.

The difference mainly involves continuous undulations crossing the 10 m threshold. For example, a 12.81 m descent becomes a local drop of approximately 7.73 m after 40 m averaging, potentially removing a confirmed downward reversal. Independent elevation data is still needed to establish whether these undulations are real.

Additional trials produced 5290.0 m with a 60 m window and 10 m threshold, and 4895.4 m with a 100 m window and 10 m threshold. Resampling every 5 m without averaging, retaining the threshold, produced 5935.7 m. Agreement with the reported COROS total of roughly 5300 m does not establish accuracy or justify deleting points or tuning parameters.

### Post-race FIT comparison

After the October 31, 2026 race, recomputing the route from recorded FIT device distance and per-record elevations produced approximately 4783 m ascent. Garmin displayed 5019 m, versus approximately 5965 m on the pre-race GPX. Inputs or statistical definitions differ; no rescaling forces agreement.

With the same no-averaging + 10 m algorithm, CP3→CP4 ascent changed from 844.8 m on the GPX to 635.2 m on the FIT, and CP5→CP6 changed from 722.6 m to 273.0 m. Position comparisons show multi-point oscillations on the original GPX with smaller fluctuations at corresponding FIT locations. Continuous oscillations above the threshold still count; no isolated spikes does not imply error-free input.

This adds comparative evidence, not surveyed elevation validation or an automatic change to defaults. See the [Huizhou Ancient City example](https://github.com/yihouzenmeban/trail-running-pace/blob/main/examples/huizhou-gucheng-100k/README.en.md#post-race-activity-comparison) for full segment ascent/descent and pacing effects. The personal FIT is not published, so that part is available for viewing and understanding metric definitions only.

## Selecting a method

No additional settings are needed for the default, which is equivalent to:

```json
{
  "ascent_method": "hysteresis",
  "ascent_smoothing_m": 0,
  "ascent_threshold_m": 10
}
```

- **No averaging + 10 m threshold:** retains extrema from cleaned source elevations; noise exceeding the threshold may still count as ascent.
- **Explicit averaging:** set `ascent_smoothing_m` to a positive value such as 10, 20, or 40. Averaging can suppress real short hills. Windows are full width: 40 m means 20 m on each side.
- **Window method:** does not use reversal filtering. See [configuration](configuration.en.md#previous-window-method-and-explicit-filtering) for settings and legacy compatibility.

The 10 m threshold applies to cumulative reversal, not adjacent-point elevation differences. Display profiles independently use 5 m sampling and 20 m averaging; duplicate handling and isolated spike correction remain enabled by default. See the [model](model.en.md#ascent-and-descent) for details and [configuration](configuration.en.md#parameters) for settings.
