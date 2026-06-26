# Deployment Guide

## Production Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Data Sources  │────▶│  Feature Pipeline │────▶│  Model Serving  │
│  - SCADA/EMS    │     │  - Preprocessing  │     │  - REST API     │
│  - Weather API  │     │  - Feature Eng    │     │  - Batch Jobs   │
│  - Calendar     │     │  - Validation     │     │  - Monitoring   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   Downstream    │
                                               │  - Grid Ops     │
                                               │  - Trading      │
                                               │  - Dashboards   │
                                               └─────────────────┘
```

## Model Serialization

### LightGBM/XGBoost

```python
import joblib
import json
from datetime import datetime

def save_model_for_deployment(model, feature_engineer, metadata, output_path):
    """Save model with all dependencies for deployment."""
    package = {
        'model': model,
        'feature_engineer': feature_engineer,
        'metadata': {
            **metadata,
            'saved_at': datetime.now().isoformat(),
            'framework': 'lightgbm',
            'version': '1.0.0'
        }
    }
    
    joblib.dump(package, output_path)
    print(f"Model saved to {output_path}")

def load_model_for_deployment(model_path):
    """Load complete model package."""
    package = joblib.load(model_path)
    return package['model'], package['feature_engineer'], package['metadata']

# Usage
metadata = {
    'model_type': 'lightgbm',
    'horizon': 24,
    'mape_val': 2.3,
    'training_samples': 50000,
    'features': feature_engineer.feature_columns
}

save_model_for_deployment(
    trained_model,
    feature_engineer,
    metadata,
    'models/lightgbm-stlf-v1.joblib'
)
```

### PyTorch Models

```python
import torch
from pathlib import Path

def save_pytorch_model(model, scaler, config, output_dir):
    """Save PyTorch model with dependencies."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Save model state
    torch.save({
        'model_state_dict': model.state_dict(),
        'scaler_state': scaler,
        'config': config,
    }, f'{output_dir}/model.pt')
    
    # Save config as JSON
    import json
    with open(f'{output_dir}/config.json', 'w') as f:
        json.dump(config, f, indent=2)

def load_pytorch_model(model_class, checkpoint_path):
    """Load PyTorch model for inference."""
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    
    config = checkpoint['config']
    model = model_class(**config['model_params'])
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    return model, checkpoint['scaler_state'], config
```

### ONNX Export (Cross-Platform)

```python
import onnx

def export_to_onnx(model, X_sample, output_path):
    """Export model to ONNX format for cross-platform deployment."""
    model.eval()
    
    # Create dummy input
    dummy_input = torch.FloatTensor(X_sample)
    
    # Export
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        export_params=True,
        opset_version=11,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )
    
    # Verify
    onnx_model = onnx.load(output_path)
    onnx.checker.check_model(onnx_model)
    print(f"Model exported to {output_path}")

# Load ONNX model
import onnxruntime as ort

session = ort.InferenceSession('model.onnx')
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

def predict_onnx(session, X):
    return session.run([output_name], {input_name: X.astype(np.float32)})[0]
```

## Feature Pipeline

### Consistent Preprocessing

```python
class DeploymentFeaturePipeline:
    """Feature pipeline that guarantees train/inference consistency."""
    
    def __init__(self, config_path='feature_config.json'):
        self.config = self._load_config(config_path)
        self.scalers = {}
        self.feature_columns = None
    
    def fit(self, df):
        """Fit scalers on training data."""
        for col in self.config['scaled_features']:
            scaler = RobustScaler()
            df[col] = scaler.fit_transform(df[[col]])
            self.scalers[col] = scaler
        
        self.feature_columns = self.config['feature_columns']
        return self
    
    def transform(self, df):
        """Transform new data using fitted scalers."""
        df = df.copy()
        
        # Apply same transformations as training
        df = self._add_temporal_features(df)
        df = self._add_lag_features(df)
        df = self._add_rolling_features(df)
        df = self._add_weather_features(df)
        
        # Apply fitted scalers
        for col, scaler in self.scalers.items():
            if col in df.columns:
                df[col] = scaler.transform(df[[col]])
        
        # Ensure correct column order
        return df[self.feature_columns]
    
    def save_config(self, path):
        """Save pipeline configuration."""
        import json
        config = {
            'feature_columns': self.feature_columns,
            'scaler_params': {
                col: {
                    'center': scaler.center_.tolist(),
                    'scale': scaler.scale_.tolist()
                }
                for col, scaler in self.scalers.items()
            }
        }
        with open(path, 'w') as f:
            json.dump(config, f, indent=2)
```

## Real-time Inference Service

### FastAPI Service

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime, timedelta

app = FastAPI(title="Electricity Forecasting API")

# Load model at startup
model, feature_engineer, metadata = load_model_for_deployment('models/lightgbm-stlf-v1.joblib')

class ForecastRequest(BaseModel):
    timestamp: datetime
    temperature: float
    humidity: float | None = None
    historical_load: list[float]  # Last 168 hours
    
class ForecastResponse(BaseModel):
    timestamp: datetime
    predictions: list[float]
    lower_bound: list[float]
    upper_bound: list[float]
    model_version: str

@app.post("/forecast", response_model=ForecastResponse)
async def get_forecast(request: ForecastRequest):
    """Generate 24-hour electricity load forecast."""
    try:
        # Prepare input data
        df = prepare_input_dataframe(
            request.timestamp,
            request.temperature,
            request.humidity,
            request.historical_load
        )
        
        # Apply feature engineering
        X = feature_engineer.transform(df)
        
        # Generate predictions
        predictions = model.predict(X)
        
        # For uncertainty, use quantile models or conformal
        lower, upper = generate_prediction_intervals(X, predictions)
        
        return ForecastResponse(
            timestamp=request.timestamp,
            predictions=predictions.tolist(),
            lower_bound=lower.tolist(),
            upper_bound=upper.tolist(),
            model_version=metadata['version']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def prepare_input_dataframe(timestamp, temperature, humidity, historical_load):
    """Prepare input dataframe for feature engineering."""
    # Create time index for forecast horizon
    forecast_hours = pd.date_range(
        start=timestamp + timedelta(hours=1),
        periods=24,
        freq='H'
    )
    
    # Create base dataframe
    df = pd.DataFrame(index=forecast_hours)
    df['load'] = historical_load[-24:] + [None] * 24  # Historical + placeholder
    df['temperature'] = temperature  # In production, use weather forecast
    df['humidity'] = humidity
    
    return df

# Run with: uvicorn main:app --host 0.0.0.0 --port 8000
```

### Batch Forecasting Script

```python
#!/usr/bin/env python3
"""
Daily batch forecasting job.
Run via cron: 0 5 * * * /usr/bin/python3 /path/to/batch_forecast.py
"""

import sys
import logging
from datetime import datetime, timedelta
import pandas as pd
import joblib

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/electricity_forecast.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    logging.info("Starting batch forecast job")
    
    # Load model
    try:
        model, feature_engineer, metadata = load_model_for_deployment(
            'models/lightgbm-stlf-v1.joblib'
        )
    except Exception as e:
        logging.error(f"Failed to load model: {e}")
        sys.exit(1)
    
    # Load latest data
    try:
        latest_data = load_latest_data()
        weather_forecast = load_weather_forecast()
    except Exception as e:
        logging.error(f"Failed to load input data: {e}")
        sys.exit(1)
    
    # Generate forecast
    try:
        forecast_df = generate_forecast(
            model, feature_engineer, latest_data, weather_forecast
        )
    except Exception as e:
        logging.error(f"Forecast generation failed: {e}")
        sys.exit(1)
    
    # Save forecast
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    output_path = f'forecasts/forecast_{timestamp}.csv'
    forecast_df.to_csv(output_path, index=False)
    logging.info(f"Forecast saved to {output_path}")
    
    # Send to downstream systems
    try:
        send_to_downstream(forecast_df)
    except Exception as e:
        logging.error(f"Failed to send forecast: {e}")
        # Don't exit - forecast was still generated
    
    logging.info("Batch forecast job completed successfully")

def load_latest_data():
    """Load latest SCADA/historical data."""
    # Implementation depends on your data source
    pass

def load_weather_forecast():
    """Load weather forecast from API."""
    # Implementation depends on your weather provider
    pass

def generate_forecast(model, feature_engineer, data, weather):
    """Generate forecast using model."""
    # Prepare features
    df = prepare_forecast_input(data, weather)
    X = feature_engineer.transform(df)
    
    # Predict
    predictions = model.predict(X)
    
    # Create output dataframe
    forecast_df = pd.DataFrame({
        'timestamp': df.index,
        'predicted_load': predictions,
        'generated_at': datetime.now()
    })
    
    return forecast_df

def send_to_downstream(forecast_df):
    """Send forecast to downstream systems."""
    # Examples:
    # - Push to message queue (Kafka, RabbitMQ)
    # - Write to database
    # - Call webhook
    # - Upload to S3
    pass

if __name__ == '__main__':
    main()
```

## Monitoring

### Performance Monitoring

```python
class ForecastMonitor:
    """Monitor forecast performance in production."""
    
    def __init__(self, metrics_db_path='metrics.db'):
        self.db_path = metrics_db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize metrics database."""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS forecasts (
                id INTEGER PRIMARY KEY,
                forecast_time TIMESTAMP,
                target_time TIMESTAMP,
                predicted_value REAL,
                actual_value REAL,
                model_version TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_metrics (
                date DATE PRIMARY KEY,
                mape REAL,
                rmse REAL,
                mae REAL,
                model_version TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_forecast(self, forecast_time, target_time, predicted, actual, version):
        """Record a forecast and its actual outcome."""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO forecasts 
            (forecast_time, target_time, predicted_value, actual_value, model_version)
            VALUES (?, ?, ?, ?, ?)
        ''', (forecast_time, target_time, predicted, actual, version))
        
        conn.commit()
        conn.close()
    
    def calculate_daily_metrics(self, date):
        """Calculate daily performance metrics."""
        import sqlite3
        import numpy as np
        
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT predicted_value, actual_value FROM forecasts
            WHERE DATE(target_time) = ?
        '''
        df = pd.read_sql_query(query, conn, params=(date,))
        conn.close()
        
        if len(df) == 0:
            return None
        
        # Calculate metrics
        errors = df['actual_value'] - df['predicted_value']
        mape = np.mean(np.abs(errors / df['actual_value'])) * 100
        rmse = np.sqrt(np.mean(errors ** 2))
        mae = np.mean(np.abs(errors))
        
        # Save daily metrics
        self._save_daily_metrics(date, mape, rmse, mae)
        
        return {'mape': mape, 'rmse': rmse, 'mae': mae}
    
    def _save_daily_metrics(self, date, mape, rmse, mae):
        """Save daily metrics to database."""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO daily_metrics 
            (date, mape, rmse, mae, model_version)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, mape, rmse, mae, 'current'))
        
        conn.commit()
        conn.close()
    
    def check_degradation(self, threshold_mape_increase=0.2):
        """Check if model performance has degraded."""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        
        # Get last 7 days of MAPE
        query = '''
            SELECT date, mape FROM daily_metrics 
            ORDER BY date DESC LIMIT 7
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if len(df) < 7:
            return False, "Insufficient data"
        
        # Compare recent 3 days to previous 4 days average
        recent_avg = df.head(3)['mape'].mean()
        baseline_avg = df.tail(4)['mape'].mean()
        
        degradation = (recent_avg - baseline_avg) / baseline_avg
        
        if degradation > threshold_mape_increase:
            return True, f"MAPE increased by {degradation*100:.1f}%"
        
        return False, f"Performance stable (change: {degradation*100:.1f}%)"
```

### Drift Detection

```python
import numpy as np
from scipy import stats

def calculate_psi(expected, actual, buckets=10):
    """
    Calculate Population Stability Index.
    PSI > 0.2 indicates significant drift.
    """
    # Create buckets
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    
    # Calculate distributions
    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts = np.histogram(actual, bins=breakpoints)[0]
    
    # Convert to proportions
    expected_props = expected_counts / len(expected)
    actual_props = actual_counts / len(actual)
    
    # Avoid division by zero
    expected_props = np.where(expected_props == 0, 0.0001, expected_props)
    actual_props = np.where(actual_props == 0, 0.0001, actual_props)
    
    # Calculate PSI
    psi = np.sum((actual_props - expected_props) * np.log(actual_props / expected_props))
    
    return psi

def monitor_feature_drift(reference_data, current_data, threshold=0.2):
    """Monitor feature drift for all features."""
    drift_report = {}
    
    for col in reference_data.columns:
        psi = calculate_psi(
            reference_data[col].values,
            current_data[col].values
        )
        
        status = 'OK' if psi < threshold else 'DRIFT_DETECTED'
        drift_report[col] = {
            'psi': psi,
            'status': status
        }
    
    return drift_report
```

## Retraining Pipeline

### Automated Retraining

```python
class RetrainingPipeline:
    """Automated model retraining pipeline."""
    
    def __init__(self, config):
        self.config = config
        self.monitor = ForecastMonitor()
    
    def check_retrain_trigger(self):
        """Check if retraining is needed."""
        triggers = []
        
        # Trigger 1: Performance degradation
        degraded, reason = self.monitor.check_degradation()
        if degraded:
            triggers.append(f"Performance: {reason}")
        
        # Trigger 2: Scheduled retrain (quarterly)
        if self._is_quarterly_retrain_due():
            triggers.append("Scheduled quarterly retrain")
        
        # Trigger 3: Data drift
        drift_detected = self._check_data_drift()
        if drift_detected:
            triggers.append("Data drift detected")
        
        return len(triggers) > 0, triggers
    
    def run_retraining(self):
        """Execute full retraining pipeline."""
        logging.info("Starting retraining pipeline")
        
        # 1. Load fresh data
        data = self._load_training_data()
        
        # 2. Split data
        train, val, test = self._split_data(data)
        
        # 3. Train model
        model, feature_engineer = self._train_model(train, val)
        
        # 4. Evaluate
        metrics = self._evaluate_model(model, test)
        
        # 5. Validate improvement
        if not self._validate_improvement(metrics):
            logging.warning("New model does not improve over current")
            return False
        
        # 6. Deploy
        self._deploy_model(model, feature_engineer, metrics)
        
        logging.info("Retraining completed successfully")
        return True
    
    def _validate_improvement(self, new_metrics):
        """Validate new model is better than current."""
        current_metrics = self._get_current_metrics()
        
        # Require at least 5% improvement in MAPE
        improvement = (current_metrics['mape'] - new_metrics['mape']) / current_metrics['mape']
        
        return improvement > 0.05
```

## Cron Configuration

```bash
# /etc/cron.d/electricity_forecast

# Daily forecast at 5 AM
0 5 * * * root /usr/bin/python3 /opt/electricity_forecast/batch_forecast.py >> /var/log/forecast.log 2>&1

# Hourly forecast update
0 * * * * root /usr/bin/python3 /opt/electricity_forecast/hourly_update.py >> /var/log/forecast.log 2>&1

# Daily metrics calculation at 6 AM
0 6 * * * root /usr/bin/python3 /opt/electricity_forecast/calculate_metrics.py >> /var/log/forecast.log 2>&1

# Weekly drift check on Monday at 7 AM
0 7 * * 1 root /usr/bin/python3 /opt/electricity_forecast/check_drift.py >> /var/log/forecast.log 2>&1

# Monthly retraining check on 1st at 8 AM
0 8 1 * * root /usr/bin/python3 /opt/electricity_forecast/check_retrain.py >> /var/log/forecast.log 2>&1
```

## Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p models forecasts logs

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  forecast-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./forecasts:/app/forecasts
      - ./logs:/app/logs
    environment:
      - MODEL_PATH=/app/models/lightgbm-stlf-v1.joblib
      - LOG_LEVEL=INFO
    restart: unless-stopped
  
  forecast-worker:
    build: .
    command: python batch_forecast.py
    volumes:
      - ./models:/app/models
      - ./forecasts:/app/forecasts
      - ./logs:/app/logs
    environment:
      - MODEL_PATH=/app/models/lightgbm-stlf-v1.joblib
    restart: unless-stopped
```

## Checklist for Production Deployment

- [ ] Model serialized with all dependencies
- [ ] Feature pipeline tested for consistency
- [ ] API endpoints documented and tested
- [ ] Monitoring and alerting configured
- [ ] Logging implemented
- [ ] Backup model available for fallback
- [ ] Retraining pipeline tested
- [ ] Load testing completed
- [ ] Security review (API authentication, rate limiting)
- [ ] Documentation updated
- [ ] Rollback plan documented
