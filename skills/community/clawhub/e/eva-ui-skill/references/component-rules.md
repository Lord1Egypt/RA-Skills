# Component Rules

## Primitive Components

- `ScreenFrame`: full-screen or section-level structural wrapper
- `Panel`: rectangular data container with visible separators
- `DataLabel`: small uppercase metadata label
- `MetricValue`: numeric or short alphanumeric readout
- `StatusIndicator`: dot, bar, or chip mapped to state
- `GridOverlay`: structural overlay for tactical or analysis contexts
- `TargetReticle`: crosshair, box lock, or corner-bracket structure
- `StripeBand`: repeating warning or directional bar pattern
- `CalibrationRail`: tick, ruler, or side-scale primitive
- `ThresholdBar`: segmented bar with semantic ranges
- `LeaderAnnotation`: short label connected to a target by a fine rule

## Pattern Components

- `AlertBanner`
- `TelemetryTable`
- `RadarPanel`
- `BootSequencePanel`
- `TargetLockPanel`
- `SystemStatusBoard`
- `SignalFailurePanel`
- `AuthorizationStateCard`
- `FieldMeshPanel`

## Constraints

- Large radii are not allowed.
- Shadows should not be the primary separation mechanism.
- Every component needs a state story, not just a default story.
- Pattern primitives should carry meaning, not decoration.
