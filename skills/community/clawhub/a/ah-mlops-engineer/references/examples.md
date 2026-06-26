# Mlops Engineer — Code Examples

## Example 1

```python
import mlflow
import mlflow.sklearn
import mlflow.tracking
from mlflow.models.signature import infer_signature
from mlflow.tracking import MlflowClient
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class MLflowManager:
    def __init__(self, tracking_uri="http://localhost:5000", experiment_name="default"):
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        self.client = MlflowClient()
    
    def train_and_log_model(self, X, y, model_params=None, tags=None):
        """Train model with MLflow tracking"""
        with mlflow.start_run() as run:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Log dataset info
            mlflow.log_param("dataset_size", len(X))
            mlflow.log_param("features", X.shape[1])
            mlflow.log_param("train_size", len(X_train))
            mlflow.log_param("test_size", len(X_test))
            
            # Initialize model
            if model_params is None:
                model_params = {
                    'n_estimators': 100,
                    'max_depth': 10,
                    'random_state': 42
                }
            
            model = RandomForestClassifier(**model_params)
            
            # Log hyperparameters
            mlflow.log_params(model_params)
            
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            # Log metrics
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("f1_score", f1)
            
            # Log model with signature
            signature = infer_signature(X_train, y_pred)
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                signature=signature,
                registered_model_name="RandomForestClassifier"
            )
            
            # Log tags
            if tags:
                mlflow.set_tags(tags)
            
            # Log feature importance
            if hasattr(model, 'feature_importances_'):
                feature_importance = pd.DataFrame({
                    'feature': X.columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)
                
                feature_importance.to_csv("feature_importance.csv", index=False)
                mlflow.log_artifact("feature_importance.csv")
            
            return run.info.run_id, model
    
    def promote_model_to_production(self, model_name, version):
        """Promote model to production stage"""
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage="Production"
        )
        
        return f"Model {model_name} v{version} promoted to Production"
    
    def compare_model_versions(self, model_name, metric="accuracy"):
        """Compare different versions of a model"""
        versions = self.client.search_model_versions(f"name='{model_name}'")
        
        comparison = []
        for version in versions:
            run_id = version.run_id
            run = mlflow.get_run(run_id)
            
            comparison.append({
                'version': version.version,
                'stage': version.current_stage,
                'run_id': run_id,
                metric: run.data.metrics.get(metric),
                'created_at': version.creation_timestamp
            })
        
        return pd.DataFrame(comparison).sort_values('version', ascending=False)
```

## Example 2

```python
import kfp
from kfp import dsl
from kfp.components import func_to_container_op, InputPath, OutputPath
import kfp.components as comp

# Define pipeline components
@func_to_container_op
def data_preprocessing(
    input_data_path: InputPath(),
    output_data_path: OutputPath(),
    test_size: float = 0.2
):
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    import joblib
    
    # Load data
    data = pd.read_csv(input_data_path)
    
    # Preprocessing steps
    # Handle missing values
    data = data.dropna()
    
    # Feature engineering
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save processed data
    processed_data = {
        'X_train': X_train_scaled,
        'X_test': X_test_scaled,
        'y_train': y_train.values,
        'y_test': y_test.values
    }
    
    joblib.dump(processed_data, output_data_path)
    joblib.dump(scaler, output_data_path.replace('.pkl', '_scaler.pkl'))

@func_to_container_op
def train_model(
    processed_data_path: InputPath(),
    model_path: OutputPath(),
    n_estimators: int = 100,
    max_depth: int = 10
):
    import joblib
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
    import mlflow
    import mlflow.sklearn
    
    # Load processed data
    data = joblib.load(processed_data_path)
    X_train, y_train = data['X_train'], data['y_train']
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Save model
    joblib.dump(model, model_path)
    
    # Log to MLflow
    with mlflow.start_run():
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.sklearn.log_model(model, "model")

@func_to_container_op
def evaluate_model(
    processed_data_path: InputPath(),
    model_path: InputPath(),
    metrics_path: OutputPath()
):
    import joblib
    import json
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    import mlflow
    
    # Load data and model
    data = joblib.load(processed_data_path)
    model = joblib.load(model_path)
    
    X_test, y_test = data['X_test'], data['y_test']
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }
    
    # Save metrics
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f)
    
    # Log metrics to MLflow
    with mlflow.start_run():
        for key, value in metrics.items():
            mlflow.log_metric(key, value)

# Define the pipeline
@dsl.pipeline(
    name='ML Training Pipeline',
    description='End-to-end ML training pipeline'
)
def ml_training_pipeline(
    input_data_path: str,
    test_size: float = 0.2,
    n_estimators: int = 100,
    max_depth: int = 10
):
    # Data preprocessing step
    preprocessing_task = data_preprocessing(
        input_data_path=input_data_path,
        test_size=test_size
    )
    
    # Model training step
    training_task = train_model(
        processed_data_path=preprocessing_task.outputs['output_data_path'],
        n_estimators=n_estimators,
        max_depth=max_depth
    )
    
    # Model evaluation step
    evaluation_task = evaluate_model(
        processed_data_path=preprocessing_task.outputs['output_data_path'],
        model_path=training_task.outputs['model_path']
    )
    
    return evaluation_task

# Compile and run pipeline
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(ml_training_pipeline, 'ml_pipeline.yaml')
    
    client = kfp.Client(host='http://localhost:8080')
    client.create_run_from_pipeline_func(
        ml_training_pipeline,
        arguments={
            'input_data_path': '/data/training_data.csv',
            'n_estimators': 200,
            'max_depth': 15
        }
    )
```

## Example 3

```python
import feast
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from datetime import timedelta
import pandas as pd
import numpy as np

class FeatureStoreManager:
    def __init__(self, repo_path="feature_repo"):
        self.repo_path = repo_path
        self.store = feast.FeatureStore(repo_path=repo_path)
    
    def define_feature_views(self):
        """Define feature views and entities"""
        # Define entities
        user_entity = Entity(
            name="user_id",
            value_type=ValueType.INT64,
            description="User identifier"
        )
        
        product_entity = Entity(
            name="product_id", 
            value_type=ValueType.INT64,
            description="Product identifier"
        )
        
        # Define data sources
        user_features_source = FileSource(
            path="/data/user_features.parquet",
            event_timestamp_column="event_timestamp",
            created_timestamp_column="created_timestamp"
        )
        
        product_features_source = FileSource(
            path="/data/product_features.parquet",
            event_timestamp_column="event_timestamp"
        )
        
        # Define feature views
        user_features_view = FeatureView(
            name="user_features",
            entities=["user_id"],
            ttl=timedelta(days=1),
            features=[
                Feature(name="age", dtype=ValueType.INT64),
                Feature(name="avg_purchase_amount", dtype=ValueType.DOUBLE),
                Feature(name="total_purchases", dtype=ValueType.INT64),
                Feature(name="days_since_last_purchase", dtype=ValueType.INT64)
            ],
            online=True,
            batch_source=user_features_source,
            tags={"team": "ml_platform"}
        )
        
        product_features_view = FeatureView(
            name="product_features",
            entities=["product_id"],
            ttl=timedelta(hours=6),
            features=[
                Feature(name="price", dtype=ValueType.DOUBLE),
                Feature(name="category", dtype=ValueType.STRING),
                Feature(name="avg_rating", dtype=ValueType.DOUBLE),
                Feature(name="total_reviews", dtype=ValueType.INT64)
            ],
            online=True,
            batch_source=product_features_source,
            tags={"team": "ml_platform"}
        )
        
        return [user_features_view, product_features_view], [user_entity, product_entity]
    
    def materialize_features(self, start_date, end_date):
        """Materialize features to online store"""
        self.store.materialize(start_date, end_date)
        
        return "Features materialized successfully"
    
    def get_online_features(self, feature_refs, entity_rows):
        """Retrieve features for online inference"""
        online_features = self.store.get_online_features(
            features=feature_refs,
            entity_rows=entity_rows
        )
        
        return online_features.to_df()
    
    def get_historical_features(self, entity_df, feature_refs):
        """Get historical features for training"""
        training_df = self.store.get_historical_features(
            entity_df=entity_df,
            features=feature_refs
        ).to_df()
        
        return training_df

# Example usage
def create_training_dataset():
    fs_manager = FeatureStoreManager()
    
    # Entity dataframe with user-product pairs and timestamps
    entity_df = pd.DataFrame({
        "user_id": [1001, 1002, 1003, 1004],
        "product_id": [2001, 2002, 2003, 2004],
        "event_timestamp": pd.to_datetime([
            "2023-09-01 10:00:00",
            "2023-09-01 11:00:00", 
            "2023-09-01 12:00:00",
            "2023-09-01 13:00:00"
        ])
    })
    
    # Feature references
    feature_refs = [
        "user_features:age",
        "user_features:avg_purchase_amount",
        "user_features:total_purchases",
        "product_features:price",
        "product_features:category",
        "product_features:avg_rating"
    ]
    
    # Get historical features
    training_df = fs_manager.get_historical_features(entity_df, feature_refs)
    
    return training_df
```

## Example 4

```python
import pandas as pd
import numpy as np
from scipy import stats
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab, CatTargetDriftTab
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
import prometheus_client
from prometheus_client import Counter, Histogram, Gauge, generate_latest

class ModelMonitor:
    def __init__(self, model_name, reference_data):
        self.model_name = model_name
        self.reference_data = reference_data
        
        # Prometheus metrics
        self.prediction_counter = Counter(
            f'{model_name}_predictions_total',
            'Total predictions made'
        )
        
        self.prediction_latency = Histogram(
            f'{model_name}_prediction_duration_seconds',
            'Prediction latency in seconds'
        )
        
        self.data_drift_score = Gauge(
            f'{model_name}_data_drift_score',
            'Data drift score'
        )
        
        self.prediction_distribution = Histogram(
            f'{model_name}_prediction_values',
            'Distribution of prediction values',
            buckets=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
        )
    
    def detect_data_drift(self, current_data, threshold=0.1):
        """Detect data drift using statistical tests"""
        drift_results = {}
        
        for column in self.reference_data.columns:
            if column in current_data.columns:
                ref_values = self.reference_data[column].dropna()
                curr_values = current_data[column].dropna()
                
                if self.reference_data[column].dtype in ['int64', 'float64']:
                    # KS test for numerical features
                    statistic, p_value = stats.ks_2samp(ref_values, curr_values)
                    drift_detected = p_value < threshold
                else:
                    # Chi-square test for categorical features
                    ref_counts = ref_values.value_counts()
                    curr_counts = curr_values.value_counts()
                    
                    # Align indices
                    all_categories = set(ref_counts.index) | set(curr_counts.index)
                    ref_aligned = ref_counts.reindex(all_categories, fill_value=0)
                    curr_aligned = curr_counts.reindex(all_categories, fill_value=0)
                    
                    statistic, p_value = stats.chisquare(curr_aligned, ref_aligned)
                    drift_detected = p_value < threshold
                
                drift_results[column] = {
                    'statistic': statistic,
                    'p_value': p_value,
                    'drift_detected': drift_detected
                }
        
        # Update Prometheus metric
        overall_drift_score = np.mean([r['statistic'] for r in drift_results.values()])
        self.data_drift_score.set(overall_drift_score)
        
        return drift_results
    
    def generate_drift_report(self, current_data):
        """Generate Evidently drift report"""
        data_drift_dashboard = Dashboard(tabs=[DataDriftTab()])
        data_drift_dashboard.calculate(self.reference_data, current_data)
        
        # Save report
        report_path = f"{self.model_name}_drift_report.html"
        data_drift_dashboard.save(report_path)
        
        return report_path
    
    def log_prediction(self, features, prediction, latency):
        """Log prediction metrics"""
        self.prediction_counter.inc()
        self.prediction_latency.observe(latency)
        self.prediction_distribution.observe(prediction)
    
    def check_model_performance(self, y_true, y_pred, threshold_metrics=None):
        """Monitor model performance metrics"""
        if threshold_metrics is None:
            threshold_metrics = {
                'accuracy': 0.8,
                'precision': 0.7,
                'recall': 0.7
            }
        
        from sklearn.metrics import accuracy_score, precision_score, recall_score
        
        current_metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted')
        }
        
        alerts = []
        for metric, value in current_metrics.items():
            if value < threshold_metrics.get(metric, 0):
                alerts.append(f"{metric} ({value:.3f}) below threshold ({threshold_metrics[metric]})")
        
        return current_metrics, alerts
    
    def export_metrics(self):
        """Export Prometheus metrics"""
        return generate_latest()
```

## Example 5

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Model CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: 3.9
  MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

jobs:
  data-validation:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install great-expectations pandas-profiling
    
    - name: Validate data quality
      run: |
        python scripts/data_validation.py
        python scripts/generate_data_profile.py
    
    - name: Upload data profile
      uses: actions/upload-artifact@v3
      with:
        name: data-profile
        path: data_profile.html

  model-training:
    needs: data-validation
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Train model
      run: |
        python scripts/train_model.py \
          --experiment-name "CI-CD-Pipeline" \
          --model-type "RandomForest" \
          --cross-validation
    
    - name: Model validation
      run: |
        python scripts/validate_model.py \
          --min-accuracy 0.8 \
          --min-precision 0.7
    
    - name: Upload model artifacts
      uses: actions/upload-artifact@v3
      with:
        name: model-artifacts
        path: artifacts/

  model-deployment:
    needs: model-training
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2
    
    - name: Deploy to SageMaker
      run: |
        python scripts/deploy_model.py \
          --endpoint-name "ml-model-prod" \
          --instance-type "ml.t2.medium"
    
    - name: Run integration tests
      run: |
        python scripts/integration_tests.py \
          --endpoint-name "ml-model-prod"
    
    - name: Update model registry
      run: |
        python scripts/update_model_registry.py \
          --stage "Production" \
          --model-version ${{ github.sha }}

  monitoring-setup:
    needs: model-deployment
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up monitoring
      run: |
        kubectl apply -f k8s/monitoring/
        python scripts/setup_drift_detection.py
```

## Example 6

```yaml
# Kubernetes deployment for model serving
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-server
  labels:
    app: ml-model-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-model-server
  template:
    metadata:
      labels:
        app: ml-model-server
    spec:
      containers:
      - name: model-server
        image: mlmodel:latest
        ports:
        - containerPort: 8080
        env:
        - name: MODEL_NAME
          value: "random_forest_classifier"
        - name: MODEL_VERSION
          value: "v1.0.0"
        - name: MLFLOW_TRACKING_URI
          value: "http://mlflow-server:5000"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: ml-model-service
spec:
  selector:
    app: ml-model-server
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ml-model-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: ml-api.example.com
    http:
      paths:
      - path: /predict
        pathType: Prefix
        backend:
          service:
            name: ml-model-service
            port:
              number: 80
```
