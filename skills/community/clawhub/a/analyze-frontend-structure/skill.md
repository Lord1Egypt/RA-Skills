---
name: analyze-frontend-structure
description: This skill is used to scan any frontend project directory, automatically analyze routing structure and module division, and generate a universal module-page mapping document for use by intelligent navigation systems. It is suitable for various frontend frameworks and project structures.
---

## Features

1. **Universal Routing Analysis**: Automatically identifies and parses routing configuration files of different frontend frameworks, extracting routing paths, component associations, and other information.
2. **Intelligent Module Recognition**: Analyzes directory structure and component dependencies to identify project module divisions, regardless of framework.
3. **Standardized Mapping Generation**: Generates clear mapping relationships between modules and pages, including parent-child relationships, hierarchical structures, etc.
4. **Intelligent Navigation Support**: The generated mapping document can be directly used in intelligent navigation systems, supporting quick positioning and navigation.

## Technical Implementation

### Core Functions

1. **Directory Scanning**: Traverses the specified directory, identifies key files and directory structures, and adapts to different project organization methods.
2. **Route Parsing**: Parses common routing configurations such as Vue Router, React Router, Angular Router, etc.
3. **Module Recognition**: Intelligently identifies modules based on directory structure, naming conventions, and component reference relationships.
4. **Mapping Generation**: Generates standardized module-page mapping documents, supporting multiple output formats.

### Supported Frameworks

- Vue 2/3
- React
- Angular
- Svelte
- Solid

## Usage

When user needs to analyze a frontend project structure, invoke this skill directly:

1. User provides the frontend project directory path
2. Skill automatically scans and analyzes
3. Generates module-page mapping document

## Input Requirements

- User needs to provide the directory path of the frontend project to be analyzed
- Optional: specify framework type (vue, react, angular, svelte, solid), default is auto-detection
- Optional: specify output format (json, markdown, html)
- Optional: specify output file path

## Output

Generates a mapping document containing:

- **Project Info**: project name, framework type, analysis date
- **Module List**: module name, route path, component file, nested sub-modules
- **Component List**: component name, file path, which modules use it
