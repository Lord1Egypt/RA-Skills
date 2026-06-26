#!/usr/bin/env node

/**
 * Code Archaeology to AI Plan Generator Converter
 * Converts Code Archaeology analysis results into AI Plan Generator context documents
 */

const fs = require('fs');
const path = require('path');
const CodeArchaeologyIntegrator = require('./code-archaeology-integrator.cjs');

// Command line arguments
const args = process.argv.slice(2);
const archaeologyDir = args[0];
const outputDir = args[1] || 'context-documents';
const businessDomain = args[2] || 'finance';

if (!archaeologyDir) {
  console.error('Usage: node convert-to-ai-plan-generator.cjs <archaeology-dir> [output-dir] [business-domain]');
  process.exit(1);
}

if (!fs.existsSync(archaeologyDir)) {
  console.error(`Error: Archaeology directory does not exist: ${archaeologyDir}`);
  process.exit(1);
}

try {
  // Create output directory
  fs.mkdirSync(outputDir, { recursive: true });
  
  // Initialize integrator
  const integrator = new CodeArchaeologyIntegrator(archaeologyDir);
  
  // Generate context documents
  const businessRules = integrator.generateBusinessRules(businessDomain);
  fs.writeFileSync(path.join(outputDir, 'business-rules.json'), JSON.stringify(businessRules, null, 2));
  
  const technicalSpecs = integrator.generateTechnicalSpecs(businessDomain);
  fs.writeFileSync(path.join(outputDir, 'technical-specs.yaml'), JSON.stringify(technicalSpecs, null, 2));
  
  const validationStandards = integrator.generateValidationStandards(businessDomain);
  fs.writeFileSync(path.join(outputDir, 'validation-standards.md'), validationStandards);
  
  const integrationConfig = {
    version: '1.0',
    domain: businessDomain,
    integrations: integrator.generateIntegrationSpecs(),
    securityRisks: integrator.extractSecurityRisks()
  };
  fs.writeFileSync(path.join(outputDir, 'integration-config.json'), JSON.stringify(integrationConfig, null, 2));
  
  console.log(`✅ Code Archaeology results converted to AI Plan Generator format`);
  console.log(`📁 Output directory: ${outputDir}`);
  console.log(`📄 Generated files:`);
  console.log(`   - business-rules.json`);
  console.log(`   - technical-specs.yaml`);
  console.log(`   - validation-standards.md`);
  console.log(`   - integration-config.json`);
  
} catch (error) {
  console.error('❌ Conversion failed:', error.message);
  process.exit(1);
}