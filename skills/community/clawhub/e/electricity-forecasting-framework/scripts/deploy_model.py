#!/usr/bin/env python3
"""
Model deployment script - export model for production use.

Usage:
    python scripts/deploy_model.py --model models/lightgbm_model.joblib --output deployment/
"""

import argparse
import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime
import joblib
import sys


def load_model(model_path):
    """Load trained model."""
    print(f"Loading model from {model_path}")
    
    package = joblib.load(model_path)
    
    if isinstance(package, dict):
        model = package.get('model', package)
        config = package.get('config', {})
    else:
        model = package
        config = {}
    
    return model, config


def validate_model(model, model_type, test_data):
    """Validate model before deployment."""
    print("Validating model...")
    
    issues = []
    
    # Test prediction
    try:
        if model_type in ['lightgbm', 'xgboost', 'random_forest']:
            X_test = test_data.reshape(-1, test_data.shape[-1])
            pred = model.predict(X_test[:10])
        else:
            pred = model.predict(test_data[:10])
        
        if np.any(np.isnan(pred)):
            issues.append("Model produces NaN predictions")
        if np.any(np.isinf(pred)):
            issues.append("Model produces infinite predictions")
        if np.any(pred < 0):
            issues.append("Model produces negative predictions (may be valid for net metering)")
        
        print(f"  Test prediction: OK (sample: {pred[:3]})")
    except Exception as e:
        issues.append(f"Prediction failed: {str(e)}")
    
    return issues


def create_inference_wrapper(model_type, model, feature_config):
    """Create inference wrapper for deployment."""
    
    wrapper_code = f'''
#!/usr/bin/env python3
"""
Auto-generated inference wrapper for {model_type} model.
Generated at: {datetime.now().isoformat()}
"""

import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

class ElectricityForecaster:
    """Production-ready electricity load forecaster."""
    
    def __init__(self, model_path='model.joblib'):
        self.model = joblib.load(model_path)
        self.model_type = '{model_type}'
        self.feature_columns = {json.dumps(feature_config.get('feature_columns', []))}
        self.lookback = {feature_config.get('lookback', 168)}
        self.horizon = {feature_config.get('horizon', 24)}
    
    def prepare_features(self, historical_load, weather=None, timestamp=None):
        """
        Prepare features for prediction.
        
        Args:
            historical_load: List of last {feature_config.get('lookback', 168)} hourly load values
            weather: Dict with temperature, humidity (optional)
            timestamp: Forecast start time (optional)
        
        Returns:
            Feature array ready for model prediction
        """
        # Create base dataframe
        if timestamp is None:
            timestamp = datetime.now()
        
        n_features_needed = self.lookback + self.horizon
        n_history = len(historical_load)
        
        # Extend with placeholder for forecast period
        load_series = list(historical_load) + [np.nan] * self.horizon
        
        # Create time index
        start_time = timestamp - timedelta(hours=n_history)
        dates = pd.date_range(start=start_time, periods=n_features_needed, freq='H')
        
        df = pd.DataFrame(index=dates)
        df['load'] = load_series
        
        # Add weather if provided
        if weather:
            df['temperature'] = weather.get('temperature', 20)
            df['humidity'] = weather.get('humidity', 50)
        else:
            df['temperature'] = 20
            df['humidity'] = 50
        
        # Generate temporal features
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek
        df['month'] = df.index.month
        
        # Cyclical encoding
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        # Lag features
        for lag in [1, 2, 3, 6, 12, 24, 48, 72, 168, 336]:
            df[f'lag_{{lag}}h'] = df['load'].shift(lag)
        
        # Rolling features
        df['rolling_mean_6h'] = df['load'].shift(1).rolling(6).mean()
        df['rolling_mean_24h'] = df['load'].shift(1).rolling(24).mean()
        df['rolling_mean_168h'] = df['load'].shift(1).rolling(168).mean()
        df['rolling_std_24h'] = df['load'].shift(1).rolling(24).std()
        
        # Weather features
        if 'temperature' in df.columns:
            df['temp_squared'] = df['temperature'] ** 2
            df['hdd'] = np.maximum(18 - df['temperature'], 0)
            df['cdd'] = np.maximum(df['temperature'] - 18, 0)
        
        # Holiday flag (simplified)
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['is_holiday'] = 0  # Should be implemented based on your region
        
        return df
    
    def predict(self, historical_load, weather=None, timestamp=None):
        """
        Generate forecast.
        
        Args:
            historical_load: List of last {{lookback}} hourly load values
            weather: Dict with temperature, humidity (optional)
            timestamp: Forecast start time (optional)
        
        Returns:
            Dict with predictions and metadata
        """
        # Prepare features
        df = self.prepare_features(historical_load, weather, timestamp)
        
        # Select feature columns
        X = df[self.feature_columns].values
        
        # Handle any remaining NaN
        X = np.nan_to_num(X, nan=0.0)
        
        # Predict
        if self.model_type in ['lightgbm', 'xgboost', 'random_forest']:
            X_flat = X.reshape(-1, X.shape[-1])
            pred = self.model.predict(X_flat)
        else:
            pred = self.model.predict(X)
        
        # Reshape to horizon
        pred = pred.reshape(-1, self.horizon)[0]
        
        # Create output
        forecast_start = timestamp or datetime.now()
        forecast_times = pd.date_range(start=forecast_start + timedelta(hours=1), 
                                        periods=self.horizon, freq='H')
        
        return {{
            'timestamp': forecast_start.isoformat(),
            'predictions': pred.tolist(),
            'forecast_times': [t.isoformat() for t in forecast_times],
            'model_type': self.model_type,
            'horizon': self.horizon
        }}
    
    def predict_dataframe(self, historical_load, weather=None, timestamp=None):
        """Generate forecast as DataFrame."""
        result = self.predict(historical_load, weather, timestamp)
        
        df = pd.DataFrame({{
            'timestamp': result['forecast_times'],
            'predicted_load': result['predictions']
        }})
        
        return df


if __name__ == '__main__':
    # Example usage
    forecaster = ElectricityForecaster()
    
    # Generate sample historical data
    np.random.seed(42)
    historical = np.random.normal(1000, 100, 168).tolist()
    
    # Predict
    result = forecaster.predict(historical, weather={{'temperature': 25}})
    print(f"Generated {{len(result['predictions'])}} hour forecast")
    print(f"First 5 predictions: {{result['predictions'][:5]}}")
'''
    
    return wrapper_code


def create_dockerfile(output_dir):
    """Create Dockerfile for deployment."""
    
    dockerfile = '''FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \\
    pandas \\
    numpy \\
    scikit-learn \\
    lightgbm \\
    joblib \\
    fastapi \\
    uvicorn \\
    pydantic

# Copy model and wrapper
COPY model.joblib /app/
COPY forecaster.py /app/
COPY api_server.py /app/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
'''
    
    return dockerfile


def create_api_server(output_dir):
    """Create FastAPI server."""
    
    api_code = '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from forecaster import ElectricityForecaster
from datetime import datetime

app = FastAPI(title="Electricity Forecasting API")

# Load model
forecaster = ElectricityForecaster('model.joblib')


class ForecastRequest(BaseModel):
    historical_load: List[float]
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    timestamp: Optional[str] = None


class ForecastResponse(BaseModel):
    timestamp: str
    predictions: List[float]
    forecast_times: List[str]
    model_type: str
    horizon: int


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/forecast", response_model=ForecastResponse)
async def get_forecast(request: ForecastRequest):
    """Generate electricity load forecast."""
    try:
        weather = None
        if request.temperature is not None:
            weather = {
                'temperature': request.temperature,
                'humidity': request.humidity
            }
        
        timestamp = None
        if request.timestamp:
            timestamp = datetime.fromisoformat(request.timestamp)
        
        result = forecaster.predict(
            request.historical_load,
            weather=weather,
            timestamp=timestamp
        )
        
        return ForecastResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model/info")
async def model_info():
    """Get model information."""
    return {
        "model_type": forecaster.model_type,
        "horizon": forecaster.horizon,
        "lookback": forecaster.lookback,
        "n_features": len(forecaster.feature_columns)
    }
'''
    
    return api_code


def create_requirements(output_dir):
    """Create requirements.txt."""
    
    requirements = '''pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
lightgbm>=4.0.0
joblib>=1.3.0
fastapi>=0.100.0
uvicorn>=0.23.0
pydantic>=2.0.0
'''
    
    return requirements


def save_deployment_package(model, model_type, feature_config, output_dir):
    """Save complete deployment package."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save model
    model_path = output_path / 'model.joblib'
    joblib.dump(model, model_path)
    print(f"Saved model to {model_path}")
    
    # Save inference wrapper
    wrapper_code = create_inference_wrapper(model_type, model, feature_config)
    wrapper_path = output_path / 'forecaster.py'
    with open(wrapper_path, 'w') as f:
        f.write(wrapper_code)
    print(f"Saved inference wrapper to {wrapper_path}")
    
    # Save API server
    api_code = create_api_server(output_dir)
    api_path = output_path / 'api_server.py'
    with open(api_path, 'w') as f:
        f.write(api_code)
    print(f"Saved API server to {api_path}")
    
    # Save Dockerfile
    dockerfile = create_dockerfile(output_dir)
    dockerfile_path = output_path / 'Dockerfile'
    with open(dockerfile_path, 'w') as f:
        f.write(dockerfile)
    print(f"Saved Dockerfile to {dockerfile_path}")
    
    # Save requirements
    requirements = create_requirements(output_dir)
    req_path = output_path / 'requirements.txt'
    with open(req_path, 'w') as f:
        f.write(requirements)
    print(f"Saved requirements to {req_path}")
    
    # Save deployment config
    config = {
        'model_type': model_type,
        'feature_columns': feature_config.get('feature_columns', []),
        'lookback': feature_config.get('lookback', 168),
        'horizon': feature_config.get('horizon', 24),
        'deployed_at': datetime.now().isoformat(),
        'api_port': 8000
    }
    
    config_path = output_path / 'deployment_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Saved deployment config to {config_path}")
    
    # Save README
    readme = f'''# Electricity Forecasting Model Deployment

## Quick Start

### Local Testing

```bash
python forecaster.py
```

### API Server

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker build -t electricity-forecast .
docker run -p 8000:8000 electricity-forecast
```

## API Endpoints

- `GET /health` - Health check
- `POST /forecast` - Generate forecast
- `GET /model/info` - Model information

## Forecast Request

```json
{{
  "historical_load": [1000, 1010, 995, ...],  // Last {feature_config.get('lookback', 168)} hours
  "temperature": 25,
  "humidity": 60,
  "timestamp": "2024-04-02T00:00:00"
}}
```

## Model Info

- Type: {model_type}
- Horizon: {feature_config.get('horizon', 24)} hours
- Lookback: {feature_config.get('lookback', 168)} hours
- Features: {len(feature_config.get('feature_columns', []))}
'''
    
    readme_path = output_path / 'README.md'
    with open(readme_path, 'w') as f:
        f.write(readme)
    print(f"Saved README to {readme_path}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Deploy electricity forecasting model')
    parser.add_argument('--model', required=True, help='Trained model file (.joblib)')
    parser.add_argument('--output', required=True, help='Output deployment directory')
    parser.add_argument('--model-type', default='lightgbm', help='Model type')
    parser.add_argument('--feature-config', help='Feature config JSON file')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Model Deployment")
    print("=" * 60)
    
    # Load model
    model, model_config = load_model(args.model)
    
    # Load feature config if provided
    feature_config = model_config
    if args.feature_config:
        with open(args.feature_config, 'r') as f:
            feature_config = json.load(f)
    
    # Validate
    test_data = np.random.randn(10, feature_config.get('lookback', 168), len(feature_config.get('feature_columns', [1])))
    issues = validate_model(model, args.model_type, test_data)
    
    if issues:
        print("Validation issues:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    
    # Save deployment package
    output_path = save_deployment_package(model, args.model_type, feature_config, args.output)
    
    print("\n" + "=" * 60)
    print("Deployment package created successfully!")
    print(f"Output: {output_path}")
    print("\nTo start the API server:")
    print(f"  cd {output_path}")
    print("  pip install -r requirements.txt")
    print("  uvicorn api_server:app --host 0.0.0.0 --port 8000")
    print("=" * 60)


if __name__ == '__main__':
    main()
