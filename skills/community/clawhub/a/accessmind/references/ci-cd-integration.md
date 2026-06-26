# CI/CD Integration Guide

## GitHub Actions

### Basic Workflow
```yaml
name: Accessibility Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  accessibility:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install Dependencies
        run: |
          pip install accessmind playwright
          playwright install chromium
          npm install -g axe-core pa11y
      
      - name: Run Accessibility Tests
        run: accessmind test --url ${{ secrets.SITE_URL }} --standard WCAG2.2-AA
        env:
          ACCESSMIND_API_KEY: ${{ secrets.ACCESSMIND_API_KEY }}
      
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: accessibility-report
          path: reports/
      
      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('reports/summary.md', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: report
            });
```

### Advanced Workflow with Thresholds
```yaml
name: Accessibility Gate

on:
  pull_request:
    branches: [main]

jobs:
  gate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Accessibility Tests
        id: a11y
        run: |
          accessmind test \
            --url ${{ secrets.STAGING_URL }} \
            --standard WCAG2.2-AA \
            --threshold 90 \
            --fail-on critical \
            --output junit
            
      - name: Check Thresholds
        run: |
          CRITICAL=$(cat reports/violations.json | jq '.critical')
          SERIOUS=$(cat reports/violations.json | jq '.serious')
          
          if [ "$CRITICAL" -gt 0 ]; then
            echo "❌ Critical violations found: $CRITICAL"
            exit 1
          fi
          
          if [ "$SERIOUS" -gt 5 ]; then
            echo "❌ Too many serious violations: $SERIOUS (max: 5)"
            exit 1
          fi
          
          echo "✅ Accessibility gate passed"
      
      - name: Publish Results
        uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          files: reports/junit.xml
```

## GitLab CI

### Basic Configuration
```yaml
# .gitlab-ci.yml
stages:
  - test
  - report

accessibility:
  stage: test
  image: python:3.12
  before_script:
    - pip install accessmind playwright
    - playwright install chromium
    - npm install -g axe-core pa11y
  script:
    - accessmind test --url $SITE_URL --standard WCAG2.2-AA --output junit
  artifacts:
    reports:
      junit: reports/junit.xml
    paths:
      - reports/
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_PIPELINE_SOURCE == "schedule"

pages:
  stage: report
  script:
    - mkdir -p public
    - cp reports/*.html public/
  artifacts:
    paths:
      - public
  only:
    - main
```

### Advanced with Environments
```yaml
accessibility_staging:
  stage: test
  environment:
    name: staging
    url: $STAGING_URL
  script:
    - accessmind test --url $STAGING_URL --standard WCAG2.2-AA
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

accessibility_production:
  stage: test
  environment:
    name: production
    url: $PRODUCTION_URL
  script:
    - accessmind test --url $PRODUCTION_URL --standard WCAG2.2-AAA --threshold 95
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual
```

## Jenkins Pipeline

### Declarative Pipeline
```groovy
pipeline {
    agent any
    
    environment {
        SITE_URL = credentials('site-url')
        ACCESSMIND_API_KEY = credentials('accessmind-api-key')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install accessmind playwright'
                sh 'playwright install chromium'
                sh 'npm install -g axe-core pa11y'
            }
        }
        
        stage('Accessibility Tests') {
            steps {
                sh 'accessmind test --url $SITE_URL --standard WCAG2.2-AA --output junit'
            }
            post {
                always {
                    junit 'reports/junit.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'index.html',
                        reportName: 'Accessibility Report'
                    ])
                }
            }
        }
        
        stage('Gate') {
            steps {
                script {
                    def violations = readJSON file: 'reports/violations.json'
                    
                    if (violations.critical > 0) {
                        error "Critical violations found: ${violations.critical}"
                    }
                    
                    if (violations.serious > 5) {
                        error "Too many serious violations: ${violations.serious}"
                    }
                }
            }
        }
    }
}
```

## Azure DevOps

### Pipeline Configuration
```yaml
# azure-pipelines.yml
trigger:
  - main
  - develop

pool:
  vmImage: 'ubuntu-latest'

variables:
  pythonVersion: '3.12'

stages:
  - stage: Accessibility
    displayName: 'Accessibility Tests'
    jobs:
      - job: Test
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '$(pythonVersion)'
          
          - script: |
              pip install accessmind playwright
              playwright install chromium
              npm install -g axe-core pa11y
            displayName: 'Install Dependencies'
          
          - script: |
              accessmind test --url $(SITE_URL) --standard WCAG2.2-AA --output junit
            displayName: 'Run Accessibility Tests'
            env:
              ACCESSMIND_API_KEY: $(ACCESSMIND_API_KEY)
          
          - task: PublishTestResults@2
            inputs:
              testResultsFiles: 'reports/junit.xml'
              testRunTitle: 'Accessibility Tests'
          
          - task: PublishBuildArtifacts@1
            inputs:
              pathToPublish: 'reports'
              artifactName: 'Accessibility Report'
```

## CircleCI

### Configuration
```yaml
# .circleci/config.yml
version: 2.1

orbs:
  python: circleci/python@2.1.1
  node: circleci/node@5.1.0

jobs:
  accessibility:
    executor: python/default
    steps:
      - checkout
      
      - python/install-packages:
          pkg-manager: pip
          packages: accessmind, playwright
      
      - run:
          name: Install Playwright Browsers
          command: playwright install chromium
      
      - node/install-packages:
          pkg-manager: npm
          packages: axe-core, pa11y
      
      - run:
          name: Run Accessibility Tests
          command: accessmind test --url $SITE_URL --standard WCAG2.2-AA
          environment:
            ACCESSMIND_API_KEY: $ACCESSMIND_API_KEY
      
      - store_artifacts:
          path: reports/
          destination: accessibility-report
      
      - run:
          name: Check Violations
          command: |
            CRITICAL=$(cat reports/violations.json | jq '.critical')
            if [ "$CRITICAL" -gt 0 ]; then
              echo "Critical violations found: $CRITICAL"
              exit 1
            fi

workflows:
  test:
    jobs:
      - accessibility:
          context: accessibility
```

## Pre-commit Hook

### Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: accessibility-check
        name: Accessibility Check
        entry: accessmind pre-commit
        language: system
        types: [html]
        args: ['--threshold', '90']
```

### Git Hook Script
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Get changed HTML files
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.html$')

if [ -n "$CHANGED_FILES" ]; then
    echo "Running accessibility checks on changed files..."
    
    for FILE in $CHANGED_FILES; do
        accessmind test --file "$FILE" --standard WCAG2.2-AA
        
        if [ $? -ne 0 ]; then
            echo "❌ Accessibility check failed for $FILE"
            exit 1
        fi
    done
    
    echo "✅ All accessibility checks passed"
fi
```

## Scheduled Scans

### Cron Job
```bash
# Run daily accessibility scan
0 0 * * * /usr/local/bin/accessmind test --url https://example.com --standard WCAG2.2-AA --report email

# Run weekly comprehensive scan
0 0 * * 0 /usr/local/bin/accessmind audit --url https://example.com --standard WCAG2.2-AAA
```

### Kubernetes CronJob
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: accessibility-scan
spec:
  schedule: "0 0 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: accessmind
              image: accessmind/cli:latest
              args:
                - test
                - --url
                - https://example.com
                - --standard
                - WCAG2.2-AA
              env:
                - name: ACCESSMIND_API_KEY
                  valueFrom:
                    secretKeyRef:
                      name: accessmind-secrets
                      key: api-key
          restartPolicy: OnFailure
```