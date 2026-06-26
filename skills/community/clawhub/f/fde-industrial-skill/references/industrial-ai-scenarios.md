# Industrial AI Scenarios

## 1. Visual Inspection (智能质检)

**Architecture**: Camera -> Edge GPU -> CNN/ViT -> Defect Classification -> MES Alert
**Algorithms**: YOLOv8 (real-time), ViT (high-accuracy), few-shot for rare defects
**Data**: 500+ defect images per category for supervised; self-supervised for cold start
**KPI**: Miss rate < 0.1%, false positive rate < 5%, inference < 50ms
**Pitfall**: Domain shift between lab and production lighting

## 2. Predictive Maintenance (预测性维护)

**Architecture**: Sensor (vibration/temp/current) -> Feature Engineering -> Time-series Model -> Maintenance Alert
**Algorithms**: LSTM/Transformer + physics-informed features; anomaly detection for cold start
**Data**: 6-12 months sensor history; failure labels preferred but not required
**KPI**: 7-14 day prediction window, > 85% precision, < 10% false alarm rate
**Pitfall**: Imbalanced data (rare failures); concept drift as equipment ages

## 3. Process Optimization (工艺优化)

**Architecture**: Process Parameters -> Digital Twin / RL Agent -> Optimal Setpoint
**Algorithms**: Bayesian optimization (few iterations), RL (simulation available), DOE + surrogate model
**Data**: Historical process parameters + yield/quality outcomes
**KPI**: Yield improvement 2-5%, cycle time reduction 5-15%
**Pitfall**: Over-optimization on historical data without production validation

## 4. Energy Efficiency (能效优化)

**Architecture**: Energy Meters + Process Data -> Baseline Model -> Control Optimization
**Algorithms**: Regression baseline + MPC/RL control; HVAC-specific rule + ML hybrid
**Data**: 3+ months energy consumption + production schedule + weather data
**KPI**: 5-15% energy reduction, ROI payback < 12 months
**Pitfall**: Ignoring production volume correlation with energy use

## 5. Supply Chain (供应链协同)

**Architecture**: ERP Data + External Signals -> Demand Forecast -> Inventory Optimization
**Algorithms**: Graph neural network (supplier network) + Transformer (demand forecast)
**Data**: 2+ years order/delivery/inventory data; external signals (market/weather)
**KPI**: Forecast accuracy MAPE < 10%, inventory reduction 10-20%
**Pitfall**: Bullwhip effect amplification; ignoring supplier-side constraints
