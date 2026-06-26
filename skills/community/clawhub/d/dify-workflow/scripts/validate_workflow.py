#!/usr/bin/env python3
"""
Dify Workflow DSL Validator

Validates the structure and syntax of Dify workflow DSL YAML files.
"""

import yaml
import sys
from typing import Dict, List, Any, Tuple


class WorkflowValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate(self, file_path: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a Dify workflow DSL file.

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            self.errors.append(f"File not found: {file_path}")
            return False, self.errors, self.warnings
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error: {str(e)}")
            return False, self.errors, self.warnings

        # Validate top-level structure
        self._validate_top_level(data)

        # Validate app section
        if 'app' in data:
            self._validate_app(data['app'])

        # Validate workflow section
        if 'workflow' in data:
            self._validate_workflow(data['workflow'])

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def _validate_top_level(self, data: Dict):
        """Validate top-level structure."""
        required_fields = ['kind', 'version', 'app', 'workflow']
        for field in required_fields:
            if field not in data:
                self.errors.append(f"Missing required top-level field: {field}")

        if data.get('kind') != 'app':
            self.errors.append(f"Invalid 'kind' value: expected 'app', got '{data.get('kind')}'")

    def _validate_app(self, app: Dict):
        """Validate app section."""
        required_fields = ['name', 'mode']
        for field in required_fields:
            if field not in app:
                self.errors.append(f"Missing required app field: {field}")

        if app.get('mode') != 'workflow':
            self.errors.append(f"Invalid app mode: expected 'workflow', got '{app.get('mode')}'")

    def _validate_workflow(self, workflow: Dict):
        """Validate workflow section."""
        required_fields = ['graph']
        for field in required_fields:
            if field not in workflow:
                self.errors.append(f"Missing required workflow field: {field}")
                return

        graph = workflow['graph']

        # Validate graph structure
        if 'nodes' not in graph:
            self.errors.append("Missing 'nodes' in graph")
            return
        if 'edges' not in graph:
            self.errors.append("Missing 'edges' in graph")
            return

        nodes = graph['nodes']
        edges = graph['edges']

        # Validate nodes
        node_ids = set()
        has_start = False
        has_end = False

        for i, node in enumerate(nodes):
            node_id = node.get('id')
            if not node_id:
                self.errors.append(f"Node at index {i} missing 'id'")
                continue

            if node_id in node_ids:
                self.errors.append(f"Duplicate node ID: {node_id}")
            node_ids.add(node_id)

            # Check node type
            if 'data' not in node:
                self.errors.append(f"Node {node_id} missing 'data'")
                continue

            node_type = node['data'].get('type')
            if not node_type:
                self.errors.append(f"Node {node_id} missing type")
                continue

            if node_type == 'start':
                has_start = True
                self._validate_start_node(node_id, node['data'])
            elif node_type == 'end':
                has_end = True
                self._validate_end_node(node_id, node['data'])
            elif node_type == 'llm':
                self._validate_llm_node(node_id, node['data'])
            elif node_type == 'code':
                self._validate_code_node(node_id, node['data'])
            elif node_type == 'variable-aggregator':
                self._validate_aggregator_node(node_id, node['data'])
            elif node_type == 'if-else':
                self._validate_ifelse_node(node_id, node['data'])

        if not has_start:
            self.errors.append("Workflow must have at least one 'start' node")
        if not has_end:
            self.errors.append("Workflow must have at least one 'end' node")

        # Validate edges
        for i, edge in enumerate(edges):
            source = edge.get('source')
            target = edge.get('target')

            if not source:
                self.errors.append(f"Edge at index {i} missing 'source'")
            elif source not in node_ids:
                self.errors.append(f"Edge references non-existent source node: {source}")

            if not target:
                self.errors.append(f"Edge at index {i} missing 'target'")
            elif target not in node_ids:
                self.errors.append(f"Edge references non-existent target node: {target}")

    def _validate_start_node(self, node_id: str, data: Dict):
        """Validate start node."""
        if 'variables' not in data:
            self.warnings.append(f"Start node {node_id} has no variables defined")
        else:
            for var in data['variables']:
                if 'variable' not in var:
                    self.errors.append(f"Variable in start node {node_id} missing 'variable' name")
                if 'type' not in var:
                    self.errors.append(f"Variable '{var.get('variable', '?')}' in start node {node_id} missing 'type'")

    def _validate_end_node(self, node_id: str, data: Dict):
        """Validate end node."""
        if 'outputs' not in data:
            self.warnings.append(f"End node {node_id} has no outputs defined")
        else:
            for output in data['outputs']:
                if 'variable' not in output:
                    self.errors.append(f"Output in end node {node_id} missing 'variable' name")
                if 'value_selector' not in output:
                    self.errors.append(f"Output '{output.get('variable', '?')}' in end node {node_id} missing 'value_selector'")

    def _validate_llm_node(self, node_id: str, data: Dict):
        """Validate LLM node."""
        if 'model' not in data:
            self.errors.append(f"LLM node {node_id} missing 'model' configuration")
        else:
            model = data['model']
            required = ['provider', 'name', 'mode']
            for field in required:
                if field not in model:
                    self.errors.append(f"LLM node {node_id} model missing '{field}'")

        if 'prompt_template' not in data:
            self.errors.append(f"LLM node {node_id} missing 'prompt_template'")
        elif not data['prompt_template']:
            self.warnings.append(f"LLM node {node_id} has empty prompt_template")

    def _validate_code_node(self, node_id: str, data: Dict):
        """Validate code node."""
        required = ['code', 'code_language']
        for field in required:
            if field not in data:
                self.errors.append(f"Code node {node_id} missing '{field}'")

        if 'code_language' in data and data['code_language'] not in ['python3', 'javascript']:
            self.errors.append(f"Code node {node_id} has invalid code_language: {data['code_language']}")

        if 'outputs' not in data:
            self.warnings.append(f"Code node {node_id} has no outputs defined")

    def _validate_aggregator_node(self, node_id: str, data: Dict):
        """Validate variable aggregator node."""
        if 'variables' not in data:
            self.errors.append(f"Variable aggregator node {node_id} missing 'variables'")
        elif not data['variables']:
            self.warnings.append(f"Variable aggregator node {node_id} has empty variables list")

        if 'output_type' not in data:
            self.errors.append(f"Variable aggregator node {node_id} missing 'output_type'")

    def _validate_ifelse_node(self, node_id: str, data: Dict):
        """Validate if-else node."""
        if 'conditions' not in data:
            self.errors.append(f"If-else node {node_id} missing 'conditions'")
        elif not data['conditions']:
            self.warnings.append(f"If-else node {node_id} has empty conditions list")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_workflow.py <workflow.yml>")
        sys.exit(1)

    file_path = sys.argv[1]
    validator = WorkflowValidator()
    is_valid, errors, warnings = validator.validate(file_path)

    if warnings:
        print("⚠️  Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
        print()

    if errors:
        print("❌ Validation failed with errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✅ Workflow validation passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()
