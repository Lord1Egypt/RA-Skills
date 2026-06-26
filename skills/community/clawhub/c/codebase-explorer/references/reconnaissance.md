# Reconnaissance Phase

Gather signals about the project without reading every file.

## Package Manifest Detection

- package.json, go.mod, Cargo.toml, pyproject.toml, pom.xml, Gemfile, composer.json

## Framework Fingerprinting

- next.config.*, nuxt.config.*, angular.json, vite.config.*, django settings, flask, fastapi, rails config

## Entry Point Identification

- main.*, index.*, app.*, server.*, cmd/, src/main/

## Directory Structure Snapshot

- Top 2 levels (ignore node_modules, vendor, .git, dist, build)

## Config and Tooling Detection

- .eslintrc*, .prettierrc*, tsconfig.json, Dockerfile, .github/workflows/, CI configs

## Test Structure

- tests/, test/, __tests__/, *_test.go, *.spec.ts, pytest.ini, jest.config.*
