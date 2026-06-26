# Component Capability Map

**Project**: zvt
**Scan date**: 2026-04-20
**Stats**: {'total_files': 325, 'total_classes': 424, 'total_functions': 571, 'total_business_decision_candidates': 147}

## Modules (14)

- [factors](components/factors.md): 54 classes
- [recorders](components/recorders.md): 90 classes
- [trader](components/trader.md): 22 classes
- [domain](components/domain.md): 114 classes
- [api](components/api.md): 2 classes
- [contract](components/contract.md): 53 classes
- [broker](components/broker.md): 6 classes
- [ml](components/ml.md): 5 classes
- [tag](components/tag.md): 42 classes
- [trading](components/trading.md): 19 classes
- [common](components/common.md): 9 classes
- [misc](components/misc.md): 2 classes
- [informer](components/informer.md): 4 classes
- [samples](components/samples.md): 2 classes

## Data Flow Hints (6)

- {'from': 'EntitySchema (contract/schema.py)', 'to': 'Recorder (contract/recorder.py)', 'how': 'Recorder.data_schema = EntitySchema; RecorderManager registers recorders per entity'}
- {'from': 'Recorder', 'to': 'Domain DB (SQLAlchemy models in domain/)', 'how': 'Recorder.run() calls schema.query_data() / session.add() via zvt storage layer'}
- {'from': 'Domain DB', 'to': 'Factor (contract/factor.py)', 'how': 'Factor.__init__ reads entity_schema; Factor.compute() loads data via TechnicalFactor/TransformerFactor'}
- {'from': 'Factor', 'to': 'TargetSelector (factors/target_selector.py)', 'how': 'TargetSelector aggregates multiple Factors; filters entities by score'}
- {'from': 'TargetSelector', 'to': 'Trader (trader/)', 'how': 'Trader consumes TargetSelector.run() result to make buy/sell decisions'}
- {'from': 'Trader', 'to': 'SimAccount / Broker', 'how': 'Trader places orders via Account.order(); SimAccount simulates fills'}