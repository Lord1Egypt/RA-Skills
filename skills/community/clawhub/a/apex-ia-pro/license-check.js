#!/usr/bin/env node

// ============================================
// SISTEMA DE LICENÇA E DOAÇÕES
// ============================================

import crypto from 'crypto';
import fs from 'fs';
import path from 'path';

const LICENSE_FILE = path.join(process.env.HOME, 'apex-ia-license.json');

// SEUS ENDEREÇOS PARA DOAÇÕES
const YOUR_WALLET_USDT = '0xe011b57a2d3082849d04c685925827cfc9d93edf';
const YOUR_WALLET_SOL = '79LQfMttkfKSBYGge3TsE3UoTxKMkkMn6vwSpKtpGpjb';
const YOUR_PIX = 'seu-email@provedor.com'; // Atualize com seu PIX

// ============================================
// GERAR CHAVE DE LICENÇA
// ============================================
function generateLicenseKey(email, plan) {
    const data = `${email}|${plan}|${Date.now()}|${Math.random()}`;
    const hash = crypto.createHash('sha256').update(data).digest('hex');
    const licenseKey = `${hash.substring(0, 8)}-${hash.substring(8, 16)}-${hash.substring(16, 24)}-${hash.substring(24, 32)}`;
    return licenseKey;
}

// ============================================
// VERIFICAR LICENÇA
// ============================================
function checkLicense() {
    if (!fs.existsSync(LICENSE_FILE)) {
        return { valid: false, reason: 'Licença não encontrada' };
    }
    
    const license = JSON.parse(fs.readFileSync(LICENSE_FILE, 'utf-8'));
    const now = Date.now();
    
    if (license.expiresAt && license.expiresAt < now) {
        return { valid: false, reason: 'Licença expirada' };
    }
    
    return { valid: true, plan: license.plan, email: license.email };
}

// ============================================
// ATIVAR LICENÇA
// ============================================
function activateLicense(email, licenseKey) {
    const license = {
        email: email,
        licenseKey: licenseKey,
        plan: 'pro',
        activatedAt: Date.now(),
        expiresAt: Date.now() + (365 * 24 * 60 * 60 * 1000)
    };
    
    fs.writeFileSync(LICENSE_FILE, JSON.stringify(license, null, 2));
    console.log('✅ Licença ativada com sucesso!');
    return true;
}

// ============================================
// MENSAGEM DE DOAÇÃO (EXIBIDA NA INTERFACE)
// ============================================
function showDonationMessage() {
    const colors = {
        reset: '\x1b[0m',
        green: '\x1b[32m',
        yellow: '\x1b[33m',
        cyan: '\x1b[36m'
    };
    
    console.log(`\n${colors.yellow}${'='.repeat(60)}${colors.reset}`);
    console.log(`${colors.cyan}🦞 APEX IA - VERSÃO GRATUITA${colors.reset}`);
    console.log(`${colors.yellow}${'='.repeat(60)}${colors.reset}`);
    console.log(`\n${colors.green}💡 Recursos PRO disponíveis:${colors.reset}`);
    console.log(`   • Pro: $19/mês (SMA completo + 10 pares + alertas)`);
    console.log(`   • Premium: $49/mês (+ execução automática + SMC)`);
    console.log(`   • Vitalício: $249 (tudo + suporte)`);
    console.log(`\n${colors.green}💚 Apoie o projeto com doações voluntárias:${colors.reset}`);
    console.log(`   💵 USDT (BEP20): ${YOUR_WALLET_USDT}`);
    console.log(`   ◎ SOLANA: ${YOUR_WALLET_SOL}`);
    console.log(`   🇧🇷 PIX: ${YOUR_PIX}`);
    console.log(`\n${colors.yellow}${'='.repeat(60)}${colors.reset}\n`);
}

export { generateLicenseKey, checkLicense, activateLicense, showDonationMessage };
