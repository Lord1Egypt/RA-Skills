#!/usr/bin/env python3
"""
ETL Pipeline Generator implementation for etl-pipeline-generator skill.
Provides core functionality for designing and executing ETL pipelines.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime
from collections import defaultdict


class SourceType(Enum):
    """Data source types."""
    CSV = "csv"
    JSON = "json"
    API = "api"
    DATABASE = "database"
    TEXT = "text"
    STREAM = "stream"


class TransformOperation(Enum):
    """Transformation operations."""
    NORMALIZE = "normalize"
    VALIDATE = "validate"
    DEDUPLICATE = "deduplicate"
    ENRICH = "enrich"
    CONVERT_TYPE = "convert_type"
    FILTER = "filter"
    MAP_SCHEMA = "map_schema"


class TargetSystem(Enum):
    """Target systems for loading."""
    NEO4J = "neo4j"
    RDF = "rdf"
    ARANGODB = "arangodb"
    TIGERGRAPH = "tigergraph"
    PROPERTY_GRAPH = "property_graph"
    FILE = "file"


class ExecutionMode(Enum):
    """Pipeline execution modes."""
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    STREAMING = "streaming"
    SCHEDULED = "scheduled"


@dataclass
class ExtractStage:
    """Extract stage configuration."""
    source_type: SourceType
    location: str
    format: str = "default"
    authentication: Optional[Dict[str, str]] = None
    filtering: Optional[Dict[str, Any]] = None
    batch_size: int = 1000


@dataclass
class TransformStage:
    """Transform stage configuration."""
    operations: List[str] = field(default_factory=list)
    validation_rules: List[Dict[str, Any]] = field(default_factory=list)
    enrichment_sources: List[Dict[str, Any]] = field(default_factory=list)
    error_handling: str = "skip_invalid"


@dataclass
class LoadStage:
    """Load stage configuration."""
    target_system: TargetSystem
    connection_params: Dict[str, Any]
    method: str = "bulk_import"
    batch_size: int = 5000
    error_handling: str = "fail_safe"


@dataclass
class PipelineMetrics:
    """Metrics for pipeline execution."""
    stage_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    records_processed: int = 0
    records_skipped: int = 0
    errors: int = 0
    duration_seconds: float = 0.0

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "stage": self.stage_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "records_processed": self.records_processed,
            "records_skipped": self.records_skipped,
            "errors": self.errors,
            "duration_seconds": self.duration_seconds
        }


class ETLPipelineGenerator:
    """Main ETL Pipeline Generator class."""

    def __init__(self, name: str, description: str = ""):
        """Initialize ETL pipeline generator."""
        self.name = name
        self.description = description
        self.extract_stage: Optional[ExtractStage] = None
        self.transform_stage: Optional[TransformStage] = None
        self.load_stage: Optional[LoadStage] = None
        self.metrics: List[PipelineMetrics] = []
        self.execution_log: List[str] = []
        self.execution_start: Optional[datetime] = None
        self.execution_end: Optional[datetime] = None

    def add_extract(self, source_type: str, location: str,
                   format: str = "default", **kwargs) -> None:
        """Configure extract stage."""
        self.extract_stage = ExtractStage(
            source_type=SourceType(source_type),
            location=location,
            format=format,
            authentication=kwargs.get("authentication"),
            filtering=kwargs.get("filtering"),
            batch_size=kwargs.get("batch_size", 1000)
        )

    def add_transform(self, operations: List[str],
                     validation_rules: Optional[List[Dict]] = None,
                     enrichment_sources: Optional[List[Dict]] = None,
                     error_handling: str = "skip_invalid") -> None:
        """Configure transform stage."""
        self.transform_stage = TransformStage(
            operations=operations,
            validation_rules=validation_rules or [],
            enrichment_sources=enrichment_sources or [],
            error_handling=error_handling
        )

    def add_load(self, target_system: str, connection_params: Dict[str, Any],
                method: str = "bulk_import", batch_size: int = 5000,
                error_handling: str = "fail_safe") -> None:
        """Configure load stage."""
        self.load_stage = LoadStage(
            target_system=TargetSystem(target_system),
            connection_params=connection_params,
            method=method,
            batch_size=batch_size,
            error_handling=error_handling
        )

    def validate_pipeline(self) -> bool:
        """Validate pipeline configuration."""
        if not self.extract_stage:
            self.execution_log.append("ERROR: Extract stage not configured")
            return False

        if not self.transform_stage:
            self.execution_log.append("ERROR: Transform stage not configured")
            return False

        if not self.load_stage:
            self.execution_log.append("ERROR: Load stage not configured")
            return False

        return True

    def _create_extract_metrics(self) -> PipelineMetrics:
        """Create metrics for extract stage."""
        return PipelineMetrics("extract", datetime.now())

    def _create_transform_metrics(self) -> PipelineMetrics:
        """Create metrics for transform stage."""
        return PipelineMetrics("transform", datetime.now())

    def _create_load_metrics(self) -> PipelineMetrics:
        """Create metrics for load stage."""
        return PipelineMetrics("load", datetime.now())

    def execute(self, data: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Execute the ETL pipeline."""
        if not self.validate_pipeline():
            return {
                "status": "FAILED",
                "error": "Pipeline validation failed",
                "log": self.execution_log
            }

        self.execution_start = datetime.now()
        self.execution_log.clear()
        self.metrics.clear()

        try:
            # Extract stage
            self.execution_log.append(f"Starting extract from {self.extract_stage.source_type.value}")
            extract_metrics = self._create_extract_metrics()

            if data is None:
                data = self._execute_extract()

            extract_metrics.end_time = datetime.now()
            extract_metrics.records_processed = len(data) if data else 0
            extract_metrics.duration_seconds = (
                extract_metrics.end_time - extract_metrics.start_time
            ).total_seconds()
            self.metrics.append(extract_metrics)
            self.execution_log.append(f"Extract complete: {len(data)} records")

            # Transform stage
            self.execution_log.append("Starting transform stage")
            transform_metrics = self._create_transform_metrics()

            data = self._execute_transform(data)

            transform_metrics.end_time = datetime.now()
            transform_metrics.records_processed = len(data) if data else 0
            transform_metrics.duration_seconds = (
                transform_metrics.end_time - transform_metrics.start_time
            ).total_seconds()
            self.metrics.append(transform_metrics)
            self.execution_log.append(f"Transform complete: {len(data)} records")

            # Load stage
            self.execution_log.append(
                f"Starting load to {self.load_stage.target_system.value}"
            )
            load_metrics = self._create_load_metrics()

            loaded = self._execute_load(data)

            load_metrics.end_time = datetime.now()
            load_metrics.records_processed = loaded
            load_metrics.duration_seconds = (
                load_metrics.end_time - load_metrics.start_time
            ).total_seconds()
            self.metrics.append(load_metrics)
            self.execution_log.append(f"Load complete: {loaded} records loaded")

            self.execution_end = datetime.now()
            total_duration = (self.execution_end - self.execution_start).total_seconds()

            return {
                "status": "SUCCESS",
                "pipeline_name": self.name,
                "total_duration_seconds": total_duration,
                "records_loaded": loaded,
                "metrics": [m.to_dict() for m in self.metrics],
                "log": self.execution_log
            }

        except Exception as e:
            self.execution_log.append(f"ERROR: {str(e)}")
            self.execution_end = datetime.now()

            return {
                "status": "FAILED",
                "pipeline_name": self.name,
                "error": str(e),
                "log": self.execution_log
            }

    def _execute_extract(self) -> List[Dict]:
        """Execute extract stage."""
        if self.extract_stage.source_type == SourceType.CSV:
            return self._extract_csv()
        elif self.extract_stage.source_type == SourceType.JSON:
            return self._extract_json()
        elif self.extract_stage.source_type == SourceType.API:
            return self._extract_api()
        else:
            return []

    def _extract_csv(self) -> List[Dict]:
        """Extract from CSV file."""
        try:
            import csv
            data = []
            with open(self.extract_stage.location, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            self.execution_log.append(f"CSV extraction error: {str(e)}")
            return []

    def _extract_json(self) -> List[Dict]:
        """Extract from JSON file."""
        try:
            with open(self.extract_stage.location, 'r') as f:
                data = json.load(f)
            return data if isinstance(data, list) else [data]
        except Exception as e:
            self.execution_log.append(f"JSON extraction error: {str(e)}")
            return []

    def _extract_api(self) -> List[Dict]:
        """Extract from API endpoint."""
        # Placeholder for API extraction
        self.execution_log.append(
            f"API extraction from {self.extract_stage.location}"
        )
        return []

    def _execute_transform(self, data: List[Dict]) -> List[Dict]:
        """Execute transform stage."""
        transformed_data = []

        for record in data:
            try:
                # Apply transformations
                for operation in self.transform_stage.operations:
                    record = self._apply_transformation(operation, record)

                # Apply validation
                if self._validate_record(record):
                    transformed_data.append(record)
                else:
                    if self.transform_stage.error_handling == "fail_fast":
                        raise ValueError(f"Validation failed for record: {record}")

            except Exception as e:
                self.execution_log.append(f"Transform error: {str(e)}")
                if self.transform_stage.error_handling == "fail_fast":
                    raise

        return transformed_data

    def _apply_transformation(self, operation: str, record: Dict) -> Dict:
        """Apply single transformation operation."""
        if operation == "normalize_entities":
            # Normalize string values
            for key, value in record.items():
                if isinstance(value, str):
                    record[key] = value.strip().title()

        elif operation == "validate_schema":
            # Validate required fields
            pass

        elif operation == "deduplicate":
            # Mark for deduplication
            pass

        return record

    def _validate_record(self, record: Dict) -> bool:
        """Validate a single record."""
        for rule in self.transform_stage.validation_rules:
            if not self._check_validation_rule(record, rule):
                return False
        return True

    def _check_validation_rule(self, record: Dict, rule: Dict) -> bool:
        """Check a single validation rule."""
        rule_type = rule.get("type")

        if rule_type == "required_fields":
            for field in rule.get("fields", []):
                if field not in record or record[field] is None:
                    return False

        elif rule_type == "data_type":
            field = rule.get("field")
            expected_type = rule.get("type")
            if field in record:
                value = record[field]
                if expected_type == "integer":
                    try:
                        int(value)
                    except (ValueError, TypeError):
                        return False

        return True

    def _execute_load(self, data: List[Dict]) -> int:
        """Execute load stage."""
        self.execution_log.append(
            f"Loading {len(data)} records to {self.load_stage.target_system.value}"
        )
        # Simulate loading
        return len(data)

    def to_yaml(self) -> str:
        """Generate YAML pipeline configuration."""
        yaml_content = f"""name: {self.name}
description: {self.description}

extract:
  source_type: {self.extract_stage.source_type.value}
  location: {self.extract_stage.location}
  format: {self.extract_stage.format}
  batch_size: {self.extract_stage.batch_size}

transform:
  operations:
"""
        for op in self.transform_stage.operations:
            yaml_content += f"    - {op}\n"

        yaml_content += f"""
load:
  target: {self.load_stage.target_system.value}
  method: {self.load_stage.method}
  batch_size: {self.load_stage.batch_size}
  error_handling: {self.load_stage.error_handling}
"""
        return yaml_content

    def to_dag(self) -> str:
        """Generate DAG representation."""
        dag = f"{self.extract_stage.source_type.value.upper()} → "
        dag += " → ".join(self.transform_stage.operations)
        dag += f" → {self.load_stage.target_system.value.upper()}"
        return dag

    def to_python_script(self) -> str:
        """Generate Python implementation script."""
        script = f'''#!/usr/bin/env python3
"""
Generated ETL Pipeline: {self.name}
Description: {self.description}
"""

def extract():
    """Extract stage - load data from source."""
    # TODO: Implement extract from {self.extract_stage.source_type.value}
    data = []
    return data

def transform(data):
    """Transform stage - apply transformations."""
    transformed = []
    for record in data:
'''
        for op in self.transform_stage.operations:
            script += f"        # TODO: Apply {op}\n"

        script += """        transformed.append(record)
    return transformed

def load(data):
    \"\"\"Load stage - load to target system.\"\"\"
    # TODO: Implement load to """ + self.load_stage.target_system.value + """
    loaded_count = len(data)
    return loaded_count

def main():
    \"\"\"Execute ETL pipeline.\"\"\"
    print("Starting ETL pipeline: """ + self.name + """")
    
    data = extract()
    print(f"Extracted {len(data)} records")
    
    data = transform(data)
    print(f"Transformed {len(data)} records")
    
    loaded = load(data)
    print(f"Loaded {loaded} records")
    
    return {"status": "SUCCESS", "records_loaded": loaded}

if __name__ == "__main__":
    result = main()
    print(result)
"""
        return script

    def get_summary(self) -> Dict:
        """Get pipeline summary."""
        return {
            "name": self.name,
            "description": self.description,
            "extract_source": self.extract_stage.source_type.value if self.extract_stage else None,
            "transform_operations": self.transform_stage.operations if self.transform_stage else [],
            "load_target": self.load_stage.target_system.value if self.load_stage else None,
            "metrics": [m.to_dict() for m in self.metrics],
            "execution_log": self.execution_log[-10:] if self.execution_log else []
        }

    def print_summary(self) -> None:
        """Print pipeline summary."""
        print(f"\n{'='*60}")
        print(f"ETL PIPELINE: {self.name}")
        print(f"{'='*60}")

        if self.extract_stage:
            print(f"Extract: {self.extract_stage.source_type.value} → {self.extract_stage.location}")

        if self.transform_stage:
            print(f"Transform: {len(self.transform_stage.operations)} operations")
            for op in self.transform_stage.operations:
                print(f"  - {op}")

        if self.load_stage:
            print(f"Load: {self.load_stage.target_system.value} ({self.load_stage.method})")

        if self.metrics:
            print(f"\nExecution Metrics:")
            for metric in self.metrics:
                print(f"  {metric.stage_name}: {metric.records_processed} records, {metric.duration_seconds:.2f}s")


if __name__ == "__main__":
    # Example 1: CSV to Neo4j Pipeline
    print("Example 1: CSV to Neo4j Pipeline")

    pipeline1 = ETLPipelineGenerator(
        name="customer_ingestion",
        description="Load customer data from CSV to Neo4j"
    )

    pipeline1.add_extract("csv", "data/customers.csv")
    pipeline1.add_transform(
        operations=[
            "normalize_entity_names",
            "convert_dates_to_iso8601",
            "validate_schema"
        ],
        validation_rules=[
            {"type": "required_fields", "fields": ["id", "name", "email"]}
        ]
    )
    pipeline1.add_load(
        target_system="neo4j",
        connection_params={"uri": "bolt://localhost:7687", "database": "kg"},
        method="bulk_import"
    )

    pipeline1.print_summary()
    print("\nGenerated YAML:")
    print(pipeline1.to_yaml())
    print("\nGenerated DAG:")
    print(pipeline1.to_dag())

    # Example 2: API to RDF Pipeline
    print("\n\nExample 2: API to RDF Pipeline")

    pipeline2 = ETLPipelineGenerator(
        name="api_to_rdf",
        description="Fetch data from API and convert to RDF"
    )

    pipeline2.add_extract("api", "https://api.example.com/data")
    pipeline2.add_transform(
        operations=[
            "parse_json",
            "extract_entities",
            "infer_relationships"
        ]
    )
    pipeline2.add_load(
        target_system="rdf",
        connection_params={"sparql_endpoint": "http://localhost:8080/sparql"},
        method="streaming"
    )

    pipeline2.print_summary()
    print("\nGenerated Python Script:")
    print(pipeline2.to_python_script()[:500] + "...")


