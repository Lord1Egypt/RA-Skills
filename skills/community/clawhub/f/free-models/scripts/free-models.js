/**
 * Free Models Discovery for OpenRouter
 * Discover and use free/cheap models for AI agents
 * 
 * Usage:
 *   node free-models.js
 * 
 * Environment:
 *   OPENROUTER_API_KEY - Your OpenRouter API key (required)
 */

/** @type {string|null} */
const API_KEY = process.env.OPENROUTER_API_KEY || null;

/**
 * Fetch all available models from OpenRouter
 * @returns {Promise<Array>}
 */
async function fetchAllModels() {
  const res = await fetch('https://openrouter.ai/api/v1/models');
  if (!res.ok) {
    throw new Error(`Failed to fetch models: ${res.statusText}`);
  }
  const data = await res.json();
  
  return data.data.map((m) => ({
    id: m.id,
    name: m.name,
    description: m.description,
    context_length: m.context_length,
    pricing: m.pricing,
    top_provider: m.top_provider,
    author: m.id.split('/')[0],
  }));
}

/**
 * Discover models with free or near-free pricing
 * @returns {Promise<Array>}
 */
async function discoverFreeModels() {
  const models = await fetchAllModels();
  return models.filter((m) => {
    const promptPrice = parseFloat(m.pricing.prompt);
    return promptPrice === 0 || promptPrice < 0.0001;
  });
}

/**
 * Filter models by various criteria
 * @param {Object} filter
 * @returns {Promise<Array>}
 */
async function filterModels(filter = {}) {
  let models = await fetchAllModels();
  
  if (filter.maxPromptPrice !== undefined) {
    models = models.filter((m) => {
      const price = parseFloat(m.pricing.prompt);
      return price <= filter.maxPromptPrice;
    });
  }
  
  if (filter.minContext !== undefined) {
    models = models.filter((m) => m.context_length >= filter.minContext);
  }
  
  if (filter.author) {
    models = models.filter((m) => m.author === filter.author);
  }
  
  if (filter.maxCompletionPrice !== undefined) {
    models = models.filter((m) => {
      const price = parseFloat(m.pricing.completion);
      return price <= filter.maxCompletionPrice;
    });
  }
  
  if (filter.nameContains) {
    models = models.filter((m) =>
      m.name.toLowerCase().includes(filter.nameContains.toLowerCase())
    );
  }
  
  return models;
}

/**
 * Get the best free model based on specific requirements
 * @param {Object} options
 * @returns {Promise<Object|null>}
 */
async function getBestFreeModel(options = {}) {
  let models = await discoverFreeModels();
  
  // Sort by context length (more context is better by default)
  models.sort((a, b) => b.context_length - a.context_length);
  
  // Filter for specific capabilities
  if (options.needVision) {
    const visionKeywords = ['vision', 'multimodal', 'see', 'image'];
    models = models.filter((m) =>
      visionKeywords.some((kw) =>
        m.name.toLowerCase().includes(kw) || m.id.includes(kw)
      )
    );
  }
  
  if (options.needReasoning || options.preferReasoning) {
    models = models.filter((m) =>
      m.context_length >= 100000 ||
      m.name.toLowerCase().includes('reasoning') ||
      m.name.toLowerCase().includes('opus') ||
      m.name.toLowerCase().includes('sonnet')
    );
  }
  
  if (options.maxPrice !== undefined) {
    models = models.filter((m) => {
      const price = parseFloat(m.pricing.prompt);
      return price <= options.maxPrice;
    });
  }
  
  return models[0] || null;
}

/**
 * Get models by specific author/provider
 * @param {string} author
 * @returns {Promise<Array>}
 */
async function getModelsByAuthor(author) {
  return filterModels({ author });
}

/**
 * Get the cheapest models regardless of capabilities
 * @param {number} [limit=10]
 * @returns {Promise<Array>}
 */
async function getCheapestModels(limit = 10) {
  const models = await fetchAllModels();
  
  return models
    .filter((m) => parseFloat(m.pricing.prompt) > 0)
    .sort((a, b) => parseFloat(a.pricing.prompt) - parseFloat(b.pricing.prompt))
    .slice(0, limit);
}

/**
 * Format model info for display
 * @param {Object} model
 * @returns {string}
 */
function formatModel(model) {
  const promptPrice = parseFloat(model.pricing.prompt);
  const completionPrice = parseFloat(model.pricing.completion);
  
  return `
  ${model.name}
    ID: ${model.id}
    Context: ${model.context_length.toLocaleString()} tokens
    Pricing: $${promptPrice}/1M prompt | $${completionPrice}/1M completion
    ${model.description ? `\n    ${model.description}` : ''}
  `.trim();
}

/**
 * Main CLI execution
 */
async function main() {
  if (!API_KEY) {
    console.error('❌ Error: Set OPENROUTER_API_KEY environment variable');
    console.error('   Example: export OPENROUTER_API_KEY="sk-or-v1-..."');
    process.exit(1);
  }
  
  console.log('🔍 Fetching models from OpenRouter...\n');
  
  try {
    const freeModels = await discoverFreeModels();
    
    console.log(`🆓 Found ${freeModels.length} free/near-free models:\n`);
    
    if (freeModels.length === 0) {
      console.log('   No free models found. Checking cheap models...\n');
      const cheapModels = await getCheapestModels(10);
      cheapModels.forEach((m) => {
        const price = parseFloat(m.pricing.prompt);
        console.log(`  • ${m.name} - $${price}/1M tokens (${m.context_length.toLocaleString()} ctx)`);
        console.log(`    ${m.id}`);
        console.log();
      });
    } else {
      freeModels.slice(0, 20).forEach((m) => {
        const price = parseFloat(m.pricing.prompt);
        console.log(`  • ${m.name}`);
        console.log(`    ${m.id}`);
        console.log(`    Context: ${m.context_length.toLocaleString()} tokens`);
        if (price > 0) {
          console.log(`    Price: $${price}/1M tokens`);
        } else {
          console.log(`    Price: FREE`);
        }
        console.log();
      });
      
      if (freeModels.length > 20) {
        console.log(`  ... and ${freeModels.length - 20} more`);
      }
    }
    
    console.log('\n📊 Best free model for agents:');
    const best = await getBestFreeModel();
    if (best) {
      console.log(formatModel(best));
    }
    
    console.log('\n🏆 Cheapest models:');
    const cheap = await getCheapestModels(5);
    cheap.forEach((m) => {
      const p = parseFloat(m.pricing.prompt);
      console.log(`  ${m.name}: $${p}/1M tokens`);
    });
    
  } catch (error) {
    console.error('Error fetching models:', error.message);
    process.exit(1);
  }
}

// Export functions for ES modules
export {
  fetchAllModels,
  discoverFreeModels,
  filterModels,
  getBestFreeModel,
  getModelsByAuthor,
  getCheapestModels,
  formatModel,
};

// Run CLI if executed directly (ESM compatible)
const isMain = process.argv[1]?.endsWith('free-models.js');
if (isMain) {
  main();
}
