#!/usr/bin/env node

/**
 * Tabela FIPE Skill
 * Consulta preços de veículos na Tabela FIPE brasileira
 */

const axios = require('axios');

const BASE_URL = 'https://parallelum.com.br/fipe/api/v1';

// Fetch from FIPE API
async function fetchFIPE(endpoint) {
  const response = await axios.get(`${BASE_URL}${endpoint}`);
  return response.data;
}

// Get brands
async function getBrands(tipo = 'carros') {
  return fetchFIPE(`/${tipo}/marcas`);
}

// Get models
async function getModels(tipo, marcaId) {
  return fetchFIPE(`/${tipo}/marcas/${marcaId}/modelos`);
}

// Get years
async function getYears(tipo, marcaId, modeloId) {
  return fetchFIPE(`/${tipo}/marcas/${marcaId}/modelos/${modeloId}/anos`);
}

// Get price
async function getPrice(tipo, marcaId, modeloId, anoId) {
  return fetchFIPE(`/${tipo}/marcas/${marcaId}/modelos/${modeloId}/anos/${anoId}`);
}

// Search for a vehicle by name
async function searchVehicle(nome) {
  const tipo = 'carros';
  const brands = await getBrands(tipo);
  
  const nomeLower = nome.toLowerCase();
  const results = [];
  
  // Search in each brand (limited for performance)
  const brandsToSearch = brands.slice(0, 30); // Limit brands to search
  
  for (const brand of brandsToSearch) {
    try {
      const models = await getModels(tipo, brand.codigo);
      for (const model of models.modelos) {
        if (model.nome.toLowerCase().includes(nomeLower)) {
          results.push({
            brand: brand.nome,
            brandId: brand.codigo,
            model: model.nome,
            modelId: model.codigo
          });
        }
      }
    } catch (e) {
      // Skip errors
    }
  }
  
  return results;
}

// Format price response
function formatPrice(data) {
  if (!data) return 'Dados não encontrados.';
  
  return `🚗 ${data.Modelo}
📅 Ano: ${data.AnoModelo}
⛽ Combustível: ${data.Combustivel}
🔢 Código FIPE: ${data.CodigoFipe}

💰 Preço Tabela FIPE:
   ${data.Valor}
   
📊 Mês de referência: ${data.MesReferencia}

⚠️ Observação: ${data.ModeloCodigoExterno || 'Preço médio à vista'}`;
}

// Format brands
function formatBrands(brands) {
  let output = '🏷️ MARCAS DISPONÍVEIS (carros):\n\n';
  brands.slice(0, 30).forEach((b, i) => {
    output += `${String(b.codigo).padStart(3, '0')} - ${b.nome}\n`;
  });
  output += `\n... e mais ${brands.length - 30} marcas.\n`;
  return output;
}

// Format models
function formatModels(data) {
  let output = `🏎️ MODELOS (${data.modelos.length} encontrados):\n\n`;
  data.modelos.slice(0, 20).forEach(m => {
    output += `${String(m.codigo).padStart(5, '0')} - ${m.nome}\n`;
  });
  if (data.modelos.length > 20) {
    output += `\n... e mais ${data.modelos.length - 20} modelos.`;
  }
  return output;
}

// Format years
function formatYears(anos) {
  let output = '📅 ANOS DISPONÍVEIS:\n\n';
  anos.forEach(a => {
    output += `${a.codigo} - ${a.nome}\n`;
  });
  return output;
}

// Format search results
function formatSearch(results) {
  if (results.length === 0) {
    return 'Nenhum resultado encontrado. Tente um nome diferente.';
  }
  
  let output = `🔍 Resultados para "${results[0]?.brand || 'busca'}":\n\n`;
  results.slice(0, 10).forEach((r, i) => {
    output += `${i + 1}. ${r.model} (${r.brand})\n`;
    output += `   Use: node src/index.js preco ${r.brandId} ${r.modelId} <ano>\n\n`;
  });
  
  if (results.length > 10) {
    output += `... e mais ${results.length - 10} resultados.`;
  }
  
  return output;
}

// Main CLI
async function main() {
  const args = process.argv.slice(2);
  const command = args[0]?.toLowerCase() || 'help';
  const p1 = args[1];
  const p2 = args[2];
  const p3 = args[3];

  try {
    switch (command) {
      case 'marcas': {
        const brands = await getBrands('carros');
        console.log(formatBrands(brands));
        break;
      }
      
      case 'modelos': {
        if (!p1) {
          console.log('Uso: node src/index.js modelos <codigo_marca>');
          console.log('Exemplo: node src/index.js modelos 59');
          process.exit(1);
        }
        const data = await getModels('carros', p1);
        console.log(formatModels(data));
        break;
      }
      
      case 'anos': {
        if (!p1 || !p2) {
          console.log('Uso: node src/index.js anos <codigo_marca> <codigo_modelo>');
          console.log('Exemplo: node src/index.js anos 59 5940');
          process.exit(1);
        }
        const anos = await getYears('carros', p1, p2);
        console.log(formatYears(anos));
        break;
      }
      
      case 'preco': {
        if (!p1 || !p2 || !p3) {
          console.log('Uso: node src/index.js preco <marca> <modelo> <ano>');
          console.log('Exemplo: node src/index.js preco 59 5940 2014-3');
          process.exit(1);
        }
        const price = await getPrice('carros', p1, p2, p3);
        console.log(formatPrice(price));
        break;
      }
      
      case 'search':
      case 'buscar': {
        if (!p1) {
          console.log('Uso: node src/index.js search <nome>');
          console.log('Exemplo: node src/index.js search Hilux');
          process.exit(1);
        }
        const term = command === 'search' ? args.slice(1).join(' ') : p1;
        console.log(`🔍 Buscando "${term}"...\n`);
        const results = await searchVehicle(term);
        console.log(formatSearch(results));
        break;
      }
      
      case 'help':
      default: {
        console.log(`🚗 TABELA FIPE - Consulta de Preços
        
Comandos:
  marcas              - Listar marcas de carros
  modelos <marca>    - Listar modelos de uma marca
  anos <marca> <modelo> - Listar anos de um modelo
  preco <marca> <modelo> <ano> - Ver preço
  search <nome>      - Buscar veículo por nome

Exemplos:
  node src/index.js marcas
  node src/index.js modelos 59
  node src/index.js preco 59 5940 2014-3
  node src/index.js search Hilux
  node src/index.js search "Toyota Corolla"

Códigos de marcas comuns:
  59 - Volkswagen
  21 - Chevrolet
  23 - Ford
  33 - Fiat
  48 - Toyota
  43 - Honda
`);
      }
    }
  } catch (error) {
    console.error('Erro:', error.message);
  }
}

main();
