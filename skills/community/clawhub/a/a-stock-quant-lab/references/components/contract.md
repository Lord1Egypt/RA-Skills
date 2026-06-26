# contract (53 classes)

## `IntervalLevel`
`contract/__init__.py:5`
> Repeated fixed time interval, e.g, 5m, 1d.

## `AdjustType`
`contract/__init__.py:121`
> split-adjusted type for :class:`~.zvt.contract.schema.TradableEntity` quotes

## `ActorType`
`contract/__init__.py:138`

## `TradableType`
`contract/__init__.py:159`

## `Exchange`
`contract/__init__.py:203`

## `StatefulService`
`contract/base_service.py:10`
> Base service with state could be stored in state_schema

## `OneStateService`
`contract/base_service.py:65`
> StatefulService which saving all states in one object

## `EntityStateService`
`contract/base_service.py:87`
> StatefulService which saving one state one entity

## `Registry`
`contract/context.py:13`
> Class storing zvt registering meta

## `Bean`
`contract/data_type.py:4`

## `ChartType`
`contract/drawer.py:20`
> Chart type enum

## `Rect`
`contract/drawer.py:45`
> rect struct with left-bottom(x0, y0), right-top(x1, y1)

## `Draw`
`contract/drawer.py:61`

## `Drawable`
`contract/drawer.py:231`

## `StackedDrawer`
`contract/drawer.py:296`

## `Drawer`
`contract/drawer.py:407`

## `TargetType`
`contract/factor.py:22`

## `Indicator`
`contract/factor.py:28`

## `Transformer`
`contract/factor.py:34`

## `Accumulator`
`contract/factor.py:82`

## `Scorer`
`contract/factor.py:163`

## `FactorMeta`
`contract/factor.py:181`

## `Factor`
`contract/factor.py:188`

## `ScoreFactor`
`contract/factor.py:667`

## `CustomModel`
`contract/model.py:7`

## `MixinModel`
`contract/model.py:11`

## `NormalData`
`contract/normal_data.py:6`

## `DataListener`
`contract/reader.py:16`

## `DataReader`
`contract/reader.py:40`

## `Meta`
`contract/recorder.py:71`

## `Recorder`
`contract/recorder.py:91`

## `EntityEventRecorder`
`contract/recorder.py:147`

## `TimeSeriesDataRecorder`
`contract/recorder.py:245`

## `FixedCycleDataRecorder`
`contract/recorder.py:612`

## `TimestampsDataRecorder`
`contract/recorder.py:712`

## `RouteRegistry`
`contract/route_registry.py:28`
> Maps (provider, db_name) or (provider, data_schema) to storage_id.

## `Mixin`
`contract/schema.py:34`
> Base class of schema.

## `NormalMixin`
`contract/schema.py:326`

## `Entity`
`contract/schema.py:333`

## `TradableEntity`
`contract/schema.py:348`
> tradable entity

## `ActorEntity`
`contract/schema.py:534`

## `NormalEntityMixin`
`contract/schema.py:538`

## `Portfolio`
`contract/schema.py:545`
> composition of tradable entities

## `PortfolioStock`
`contract/schema.py:580`

## `PortfolioStockHistory`
`contract/schema.py:596`

## `TradableMeetActor`
`contract/schema.py:613`

## `ActorMeetTradable`
`contract/schema.py:626`

## `StorageBackend`
`contract/storage.py:38`
> Abstract storage backend. Decouples physical storage from domain/read/record logic.

## `SqliteStorageBackend`
`contract/storage.py:65`
> SQLite storage backend. Default path: {data_path}/{provider}/{provider}_{db_name}.db

## `StateMixin`
`contract/zvt_info.py:11`

## `RecorderState`
`contract/zvt_info.py:19`
> Schema for storing recorder state

## `TaggerState`
`contract/zvt_info.py:27`
> Schema for storing tagger state

## `FactorState`
`contract/zvt_info.py:35`
> Schema for storing factor state
