#!/usr/bin/env python3
"""
CSV Graph Loader implementation for csv-graph-loader-generator skill.
Provides core functionality for converting CSV data to graph structures.
"""

from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime
from collections import defaultdict


class EntityType(Enum):
    """Entity types for CSV to graph conversion."""
    PERSON = "Person"
    ORGANIZATION = "Organization"
    LOCATION = "Location"
    PRODUCT = "Product"
    CUSTOM = "Custom"


class OutputFormat(Enum):
    """Output format for graph data."""
    NEO4J_CYPHER = "neo4j_cypher"
    RDF_TURTLE = "rdf_turtle"
    PROPERTY_GRAPH_JSON = "property_graph_json"
    CSV_NODES_EDGES = "csv_nodes_edges"


@dataclass
class CSVColumn:
    """Represents a CSV column definition."""
    name: str
    data_type: str = "string"  # string, integer, float, date, boolean
    is_id: bool = False
    is_entity_ref: bool = False
    entity_type: Optional[str] = None


@dataclass
class EntityDefinition:
    """Defines an entity type in the graph."""
    entity_type: str
    id_column: str
    name_column: Optional[str] = None
    properties: List[str] = field(default_factory=list)


@dataclass
class RelationshipDefinition:
    """Defines a relationship between entities."""
    source_entity: str
    target_entity: str
    relationship_type: str
    source_column: str
    target_column: str
    properties: List[str] = field(default_factory=list)


@dataclass
class Node:
    """Represents a graph node."""
    node_id: str
    node_type: str
    properties: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "id": self.node_id,
            "type": self.node_type,
            "properties": self.properties
        }


@dataclass
class Edge:
    """Represents a graph edge/relationship."""
    source_id: str
    target_id: str
    edge_type: str
    properties: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "source": self.source_id,
            "target": self.target_id,
            "type": self.edge_type,
            "properties": self.properties
        }


class CSVGraphLoader:
    """Core CSV to graph loader implementation."""

    def __init__(self, name: str, csv_data: Optional[List[Dict]] = None):
        """Initialize CSV graph loader."""
        self.name = name
        self.csv_data = csv_data or []
        self.columns: Dict[str, CSVColumn] = {}
        self.entities: Dict[str, EntityDefinition] = {}
        self.relationships: List[RelationshipDefinition] = []
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.errors: List[str] = []
        self.processed_at: Optional[datetime] = None

    def add_csv_data(self, data: List[Dict]) -> None:
        """Add CSV data as list of dictionaries."""
        self.csv_data = data
        self._analyze_schema()

    def define_column(self, column_name: str, data_type: str = "string",
                      is_id: bool = False) -> None:
        """Define a CSV column."""
        self.columns[column_name] = CSVColumn(
            name=column_name,
            data_type=data_type,
            is_id=is_id
        )

    def define_entity(self, entity_type: str, id_column: str,
                      name_column: Optional[str] = None) -> None:
        """Define an entity type."""
        self.entities[entity_type] = EntityDefinition(
            entity_type=entity_type,
            id_column=id_column,
            name_column=name_column
        )

    def define_relationship(self, source_entity: str, relationship_type: str,
                           target_entity: str, source_column: str,
                           target_column: str) -> None:
        """Define a relationship between entities."""
        rel = RelationshipDefinition(
            source_entity=source_entity,
            target_entity=target_entity,
            relationship_type=relationship_type,
            source_column=source_column,
            target_column=target_column
        )
        self.relationships.append(rel)

    def _analyze_schema(self) -> None:
        """Analyze CSV schema and infer types."""
        if not self.csv_data:
            return

        # Get all column names from first row
        first_row = self.csv_data[0]
        for col in first_row.keys():
            if col not in self.columns:
                data_type = self._infer_type(col)
                is_id = "_id" in col.lower() or "id" == col.lower()
                self.columns[col] = CSVColumn(
                    name=col,
                    data_type=data_type,
                    is_id=is_id
                )

    def _infer_type(self, column_name: str) -> str:
        """Infer data type from column name and values."""
        if not self.csv_data:
            return "string"

        # Check column name patterns
        if "date" in column_name.lower() or "time" in column_name.lower():
            return "date"
        elif "count" in column_name.lower():
            return "integer"
        elif "price" in column_name.lower() or "salary" in column_name.lower():
            return "float"
        elif "is_" in column_name.lower():
            return "boolean"

        # Sample values to infer type
        for row in self.csv_data[:5]:
            value = row.get(column_name, "")
            if value:
                try:
                    int(value)
                    return "integer"
                except ValueError:
                    try:
                        float(value)
                        return "float"
                    except ValueError:
                        pass

        return "string"

    def process(self) -> None:
        """Process CSV data and generate graph structure."""
        self.processed_at = datetime.now()
        self.nodes.clear()
        self.edges.clear()

        # Process entities
        for row in self.csv_data:
            self._process_row(row)

        # Process relationships
        for row in self.csv_data:
            self._process_relationships(row)

    def _process_row(self, row: Dict) -> None:
        """Process single CSV row to create nodes."""
        for entity_type, entity_def in self.entities.items():
            id_value = row.get(entity_def.id_column)

            if id_value is None:
                continue

            node_id = f"{entity_type.lower()}_{id_value}"

            # Skip if already processed (deduplication)
            if node_id in self.nodes:
                continue

            properties = {}

            # Add name if defined
            if entity_def.name_column:
                name = row.get(entity_def.name_column)
                if name:
                    properties["name"] = name

            # Add other properties
            for col, value in row.items():
                if col != entity_def.id_column and col != entity_def.name_column:
                    if value is not None and value != "":
                        properties[col] = self._convert_value(col, value)

            node = Node(
                node_id=node_id,
                node_type=entity_type,
                properties=properties
            )
            self.nodes[node_id] = node

    def _process_relationships(self, row: Dict) -> None:
        """Process relationships from CSV row."""
        for rel in self.relationships:
            source_val = row.get(rel.source_column)
            target_val = row.get(rel.target_column)

            if source_val is None or target_val is None:
                continue

            source_id = f"{rel.source_entity.lower()}_{source_val}"
            target_id = f"{rel.target_entity.lower()}_{target_val}"

            # Check for duplicates
            edge_key = (source_id, target_id, rel.relationship_type)
            if any(e.source_id == source_id and e.target_id == target_id
                   and e.edge_type == rel.relationship_type for e in self.edges):
                continue

            edge = Edge(
                source_id=source_id,
                target_id=target_id,
                edge_type=rel.relationship_type
            )
            self.edges.append(edge)

    def _convert_value(self, column_name: str, value: Any) -> Any:
        """Convert value based on column type."""
        if not value:
            return None

        col = self.columns.get(column_name)
        if not col:
            return value

        if col.data_type == "integer":
            try:
                return int(value)
            except (ValueError, TypeError):
                return value
        elif col.data_type == "float":
            try:
                return float(value)
            except (ValueError, TypeError):
                return value
        elif col.data_type == "boolean":
            if isinstance(value, bool):
                return value
            return str(value).lower() in ("true", "yes", "1")

        return str(value)

    def to_graph_json(self) -> Dict:
        """Convert to property graph JSON format."""
        return {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
            "metadata": {
                "loader_name": self.name,
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "processed_at": self.processed_at.isoformat() if self.processed_at else None
            }
        }

    def generate_cypher(self) -> List[str]:
        """Generate Neo4j Cypher statements."""
        statements = []

        for entity_type, entity_def in self.entities.items():
            # Find sample data
            sample_nodes = [n for n in self.nodes.values()
                           if n.node_type == entity_type]
            if sample_nodes:
                sample = sample_nodes[0]
                stmt = f"MERGE (n:{entity_type} {{id: row.{entity_def.id_column}}})"
                for prop, value in sample.properties.items():
                    stmt += f"\nSET n.{prop} = row.{prop}"
                statements.append(stmt)

        for rel in self.relationships:
            stmt = f"MERGE (s:{rel.source_entity})-[:{rel.relationship_type}]->(t:{rel.target_entity})"
            statements.append(stmt)

        return statements

    def generate_triples(self, namespace: str = "http://example.org/") -> List[str]:
        """Generate RDF triple statements."""
        triples = []

        for node in self.nodes.values():
            # Type triple
            node_uri = f"<{namespace}{node.node_id}>"
            type_uri = f"<{namespace}{node.node_type}>"
            triples.append(f"{node_uri} rdf:type {type_uri} .")

            # Property triples
            for prop, value in node.properties.items():
                prop_uri = f"<{namespace}{prop}>"
                if isinstance(value, str):
                    triples.append(f'{node_uri} {prop_uri} "{value}" .')
                else:
                    triples.append(f"{node_uri} {prop_uri} {value} .")

        for edge in self.edges:
            source_uri = f"<{namespace}{edge.source_id}>"
            target_uri = f"<{namespace}{edge.target_id}>"
            rel_uri = f"<{namespace}{edge.edge_type}>"
            triples.append(f"{source_uri} {rel_uri} {target_uri} .")

        return triples

    def to_node_edge_csv(self) -> Tuple[str, str]:
        """Convert to separate nodes.csv and edges.csv."""
        # Generate nodes.csv
        nodes_lines = ["id,type"]
        for node in self.nodes.values():
            for prop, value in node.properties.items():
                if prop not in nodes_lines[0]:
                    nodes_lines[0] += f",{prop}"

        for node in self.nodes.values():
            line = f"{node.node_id},{node.node_type}"
            for prop in nodes_lines[0].split(",")[2:]:
                value = node.properties.get(prop, "")
                line += f",{value}"
            nodes_lines.append(line)

        # Generate edges.csv
        edges_lines = ["source,target,type"]
        for edge in self.edges:
            line = f"{edge.source_id},{edge.target_id},{edge.edge_type}"
            edges_lines.append(line)

        nodes_csv = "\n".join(nodes_lines)
        edges_csv = "\n".join(edges_lines)

        return nodes_csv, edges_csv

    def get_summary(self) -> Dict:
        """Get loader summary."""
        return {
            "name": self.name,
            "csv_rows": len(self.csv_data),
            "total_columns": len(self.columns),
            "entity_types": len(self.entities),
            "relationship_types": len(self.relationships),
            "nodes_generated": len(self.nodes),
            "edges_generated": len(self.edges),
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "errors": self.errors
        }

    def print_summary(self) -> None:
        """Print loader summary."""
        print(f"\n{'='*60}")
        print(f"CSV GRAPH LOADER: {self.name}")
        print(f"{'='*60}")

        summary = self.get_summary()
        for key, value in summary.items():
            print(f"{key}: {value}")

        print(f"\nEntity Types:")
        for etype, edef in self.entities.items():
            print(f"  {etype}: id_column={edef.id_column}")

        print(f"\nRelationships:")
        for rel in self.relationships:
            print(f"  {rel.source_entity} -[{rel.relationship_type}]-> {rel.target_entity}")


if __name__ == "__main__":
    # Example 1: Employee-Company loader
    print("Example 1: Employee-Company CSV Loader")

    loader = CSVGraphLoader(
        name="employees",
        csv_data=[
            {
                "employee_id": "E001",
                "employee_name": "Alice Johnson",
                "job_title": "Software Engineer",
                "company_id": "C001",
                "company_name": "Acme Corp"
            },
            {
                "employee_id": "E002",
                "employee_name": "Bob Smith",
                "job_title": "Product Manager",
                "company_id": "C001",
                "company_name": "Acme Corp"
            },
            {
                "employee_id": "E003",
                "employee_name": "Carol Davis",
                "job_title": "CTO",
                "company_id": "C002",
                "company_name": "TechStart Inc"
            }
        ]
    )

    loader.define_entity("Person", id_column="employee_id", name_column="employee_name")
    loader.define_entity("Company", id_column="company_id", name_column="company_name")

    loader.define_relationship(
        "Person", "WORKS_AT", "Company",
        source_column="employee_id",
        target_column="company_id"
    )

    loader.process()
    loader.print_summary()

    print("\nGenerated Graph JSON:")
    print(json.dumps(loader.to_graph_json(), indent=2))

    # Example 2: Authors-Papers loader
    print("\n\nExample 2: Research Papers CSV Loader")

    loader2 = CSVGraphLoader(
        name="research_papers",
        csv_data=[
            {"paper_id": "P001", "title": "AI Advances", "author_id": "A001", "author_name": "Dr. Alice"},
            {"paper_id": "P001", "title": "AI Advances", "author_id": "A002", "author_name": "Dr. Bob"},
            {"paper_id": "P002", "title": "ML Techniques", "author_id": "A001", "author_name": "Dr. Alice"}
        ]
    )

    loader2.define_entity("Paper", id_column="paper_id", name_column="title")
    loader2.define_entity("Researcher", id_column="author_id", name_column="author_name")

    loader2.define_relationship(
        "Researcher", "AUTHORED", "Paper",
        source_column="author_id",
        target_column="paper_id"
    )

    loader2.process()
    loader2.print_summary()

    print("\nGenerated Nodes & Edges CSV:")
    nodes_csv, edges_csv = loader2.to_node_edge_csv()
    print("\nnodes.csv:")
    print(nodes_csv)
    print("\nedges.csv:")
    print(edges_csv)


