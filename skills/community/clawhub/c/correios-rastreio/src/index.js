#!/usr/bin/env node

/**
 * Correios Rastreio Skill
 * Rastreia pacotes dos Correios via API oficial
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://api.correios.com.br';
const DATA_FILE = path.join(__dirname, 'data.json');

// Get API key from environment
function getApiKey() {
  return process.env.CORREIOS_API_KEY;
}

// Load/Save data
function loadData() {
  try {
    if (fs.existsSync(DATA_FILE)) {
      return JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
    }
  } catch (e) {}
  return { history: [], favorites: {} };
}

function saveData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

// Track package
async function trackPackage(codigo, apiKey) {
  if (!apiKey) {
    return { erro: 'API Key não configurada. Execute: export CORREIOS_API_KEY="sua_chave_aqui"' };
  }

  try {
    const response = await axios.get(
      `${BASE_URL}/rastreio/v1/objetos/${codigo}`,
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Accept': 'application/json'
        }
      }
    );
    return response.data;
  } catch (error) {
    if (error.response?.status === 401) {
      return { erro: 'API Key inválida ou expirada. Gere uma nova em https://developers.correios.com.br' };
    }
    if (error.response?.status === 404) {
      return { erro: 'Código não encontrado. Verifique o código e tente novamente.' };
    }
    return { erro: error.message };
  }
}

// Format response
function formatTrackResponse(data, codigo) {
  if (data.erro) {
    return `❌ Erro: ${data.erro}`;
  }

  if (!data.objetos || !data.objetos[0]) {
    return 'Nenhum dado encontrado.';
  }

  const obj = data.objetos[0];
  const eventos = obj.eventos || [];
  
  let output = `📦 Rastreamento: ${codigo}\n`;
  output += `🔍 ${obj.codigo}\n`;
  
  if (eventos.length > 0) {
    const ultimo = eventos[0];
    output += `\n📍 Status: ${traduzirStatus(ultimo.status)}\n`;
    output += `📅 ${formatarData(ultimo.data)} - ${ultimohora}\n`;
    output += `📍 ${ultimo.unidade?.cidade}/${ultimo.unidade?.uf}\n`;
    
    if (ultimo.destino) {
      output += `\n🎯 Destino: ${ultimo.destino?.cidade}/${ultimo.destino?.uf}`;
    }
  }
  
  output += `\n\n📋 Histórico (mais recente primeiro):\n`;
  eventos.slice(0, 5).forEach((ev, i) => {
    output += `${i + 1}. ${formatarData(ev.data)} - ${traduzirStatus(ev.status)} (${ev.unidade?.cidade}/${ev.unidade?.uf})\n`;
  });

  return output;
}

function traduzirStatus(status) {
  const map = {
    'PO': 'Postado',
    'RO': 'Em Rota',
    'BDI': 'Budex-In',
    'BDC': 'Budex-Out',
    'CE': 'Chegada na Unidade',
    'SA': 'Saiu para Entrega',
    'OEC': 'Objeto Entregue ao Carteiro',
    'OE': 'Objeto Entregue',
    'LDI': 'Lista de Distribuição',
    'LDO': 'Lista de Distribuição',
    'DCO': 'Desistência do Envio',
    'CUS': 'Customs',
    'EST': 'Estorno',
    'RET': 'Retorno',
    'NPA': 'Não Provisionado',
    'TRI': 'Triagem',
    'PC': 'Postagem Capturada',
    'DO': 'Distribuído',
    'BDEM': 'Booking Entrega Mktp',
    'BDPM': 'Booking Postagem Mktp',
    'BDE': 'Booking Entrega',
    'BDP': 'Booking Postagem',
    'FC': 'Falha na Entrega',
    'FO': 'Falha na Operação',
    'CO': 'Condição Especial',
    'LO': 'Logo',
    'BLQ': 'Bloqueado',
    'CAN': 'Cancelado'
  };
  return map[status] || status;
}

function formatarData(dataStr) {
  if (!dataStr) return '';
  try {
    const data = new Date(dataStr);
    return data.toLocaleString('pt-BR');
  } catch {
    return dataStr;
  }
}

// Main CLI
async function main() {
  const args = process.argv.slice(2);
  const command = args[0]?.toLowerCase() || 'help';
  const param = args[1];
  
  const apiKey = getApiKey();
  const data = loadData();

  try {
    switch (command) {
      case 'track':
      case 'rastrear': {
        if (!param) {
          console.log('Uso: node src/index.js track <código>');
          console.log('Exemplo: node src/index.js track PW123456789BR');
          process.exit(1);
        }
        
        const codigos = param.split(',').map(c => c.trim());
        
        for (const codigo of codigos) {
          console.log(`\n🔍 Rastreando ${codigo}...\n`);
          const result = await trackPackage(codigo, apiKey);
          console.log(formatTrackResponse(result, codigo));
          
          // Save to history
          data.history.unshift({ codigo, data: new Date().toISOString() });
          data.history = data.history.slice(0, 50);
          saveData(data);
        }
        break;
      }
      
      case 'history': {
        console.log('📜 Últimos rastreamentos:\n');
        data.history.forEach((h, i) => {
          console.log(`${i + 1}. ${h.codigo} - ${new Date(h.data).toLocaleString('pt-BR')}`);
        });
        if (data.history.length === 0) {
          console.log('Nenhum histórico ainda.');
        }
        break;
      }
      
      case 'save': {
        const codigo = param;
        const apelido = args[2];
        if (!codigo || !apelido) {
          console.log('Uso: node src/index.js save <código> <apelido>');
          process.exit(1);
        }
        data.favorites[codigo] = apelido;
        saveData(data);
        console.log(`✅ Salvo: ${codigo} → ${apelido}`);
        break;
      }
      
      case 'favorites': {
        console.log('⭐ Favoritos/Apelidos:\n');
        const favs = Object.entries(data.favorites);
        if (favs.length === 0) {
          console.log('Nenhum favorito salvo.');
        } else {
          favs.forEach(([codigo, apelido]) => {
            console.log(`• ${codigo}: ${apelido}`);
          });
        }
        break;
      }
      
      case 'help':
      default: {
        console.log(`📦 CORREIOS RASTREIO
        
Comandos:
  track <código>     - Rastrear encomenda (ex: PW123456789BR)
  history           - Ver histórico de rastreamentos
  save <código> <nome> - Salvar apelido
  favorites         - Listar favoritos
  help              - Esta ajuda

Exemplos:
  node src/index.js track PW123456789BR
  node src/index.js track "PW123456789BR,AB987654321BR"

Configuração:
  export CORREIOS_API_KEY="sua_api_key"
`);
      }
    }
  } catch (error) {
    console.error('Erro:', error.message);
  }
}

main();
