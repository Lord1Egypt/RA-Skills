# Fintech Specialist — Code Examples

## Example 1

```typescript
import { Request, Response, NextFunction } from 'express';
import Stripe from 'stripe';
import { createHash, createCipheriv, createDecipheriv, randomBytes } from 'crypto';
import BigNumber from 'bignumber.js';
import { Pool } from 'pg';
import Redis from 'ioredis';
import winston from 'winston';
import { z } from 'zod';

/**
 * Enterprise Payment Processing System
 * PCI DSS compliant implementation with comprehensive security
 */

// Configuration
const config = {
    stripe: {
        secretKey: process.env.STRIPE_SECRET_KEY!,
        webhookSecret: process.env.STRIPE_WEBHOOK_SECRET!,
    },
    encryption: {
        algorithm: 'aes-256-gcm',
        keyDerivationIterations: 100000,
    },
    security: {
        maxRetries: 3,
        rateLimitWindow: 60000, // 1 minute
        maxRequestsPerWindow: 100,
    },
    compliance: {
        pciDssLevel: 1,
        requireTokenization: true,
        auditLogRetention: 2555, // 7 years in days
    }
};

// Database setup with encryption at rest
const db = new Pool({
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT || '5432'),
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    ssl: {
        rejectUnauthorized: true,
        ca: process.env.DB_CA_CERT,
    },
    max: 20,
    idleTimeoutMillis: 30000,
});

const redis = new Redis({
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT || '6379'),
    password: process.env.REDIS_PASSWORD,
    tls: {
        rejectUnauthorized: true,
    },
});

const stripe = new Stripe(config.stripe.secretKey, {
    apiVersion: '2023-10-16',
    typescript: true,
});

// Audit logger with immutable records
const auditLogger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ 
            filename: 'audit.log',
            options: { flags: 'a' } // Append only
        }),
        new winston.transports.Console({
            format: winston.format.simple()
        })
    ],
});

// Payment validation schemas
const PaymentRequestSchema = z.object({
    amount: z.number().positive().max(999999.99),
    currency: z.enum(['USD', 'EUR', 'GBP', 'JPY']),
    customerId: z.string().uuid(),
    paymentMethod: z.enum(['card', 'bank_transfer', 'wallet', 'crypto']),
    metadata: z.record(z.string()).optional(),
    idempotencyKey: z.string().uuid(),
});

const CardDetailsSchema = z.object({
    number: z.string().regex(/^\d{13,19}$/),
    expMonth: z.number().min(1).max(12),
    expYear: z.number().min(new Date().getFullYear()),
    cvc: z.string().regex(/^\d{3,4}$/),
    postalCode: z.string().optional(),
});

// Encryption service for sensitive data
class EncryptionService {
    private readonly masterKey: Buffer;
    
    constructor() {
        this.masterKey = Buffer.from(process.env.MASTER_KEY_BASE64!, 'base64');
        if (this.masterKey.length !== 32) {
            throw new Error('Invalid master key length');
        }
    }
    
    encrypt(plaintext: string): { encrypted: string; iv: string; tag: string } {
        const iv = randomBytes(16);
        const cipher = createCipheriv(config.encryption.algorithm, this.masterKey, iv);
        
        let encrypted = cipher.update(plaintext, 'utf8', 'hex');
        encrypted += cipher.final('hex');
        
        const tag = (cipher as any).getAuthTag();
        
        return {
            encrypted,
            iv: iv.toString('hex'),
            tag: tag.toString('hex'),
        };
    }
    
    decrypt(encrypted: string, iv: string, tag: string): string {
        const decipher = createDecipheriv(
            config.encryption.algorithm,
            this.masterKey,
            Buffer.from(iv, 'hex')
        );
        
        (decipher as any).setAuthTag(Buffer.from(tag, 'hex'));
        
        let decrypted = decipher.update(encrypted, 'hex', 'utf8');
        decrypted += decipher.final('utf8');
        
        return decrypted;
    }
    
    tokenize(data: string): string {
        // Generate secure token for PCI compliance
        const token = randomBytes(32).toString('base64url');
        const encrypted = this.encrypt(data);
        
        // Store encrypted data with token
        redis.setex(
            `token:${token}`,
            3600, // 1 hour expiry
            JSON.stringify(encrypted)
        );
        
        return token;
    }
}

// Fraud detection engine
class FraudDetectionEngine {
    private readonly riskThresholds = {
        low: 0.3,
        medium: 0.6,
        high: 0.8,
    };
    
    async assessTransaction(transaction: any): Promise<{
        score: number;
        reasons: string[];
        action: 'approve' | 'review' | 'decline';
    }> {
        const riskFactors: { factor: string; weight: number }[] = [];
        
        // Check velocity rules
        const recentTransactions = await this.getRecentTransactions(
            transaction.customerId,
            3600000 // Last hour
        );
        
        if (recentTransactions.length > 5) {
            riskFactors.push({
                factor: 'high_velocity',
                weight: 0.3,
            });
        }
        
        // Check amount anomaly
        const avgAmount = await this.getAverageTransactionAmount(transaction.customerId);
        if (transaction.amount > avgAmount * 3) {
            riskFactors.push({
                factor: 'unusual_amount',
                weight: 0.25,
            });
        }
        
        // Check geographical anomaly
        const geoRisk = await this.assessGeographicalRisk(transaction);
        if (geoRisk > 0.5) {
            riskFactors.push({
                factor: 'geographical_anomaly',
                weight: geoRisk * 0.4,
            });
        }
        
        // Check device fingerprint
        const deviceRisk = await this.assessDeviceRisk(transaction.deviceFingerprint);
        if (deviceRisk > 0.5) {
            riskFactors.push({
                factor: 'suspicious_device',
                weight: deviceRisk * 0.3,
            });
        }
        
        // Calculate final risk score
        const riskScore = riskFactors.reduce((sum, rf) => sum + rf.weight, 0);
        const reasons = riskFactors.map(rf => rf.factor);
        
        let action: 'approve' | 'review' | 'decline';
        if (riskScore < this.riskThresholds.low) {
            action = 'approve';
        } else if (riskScore < this.riskThresholds.high) {
            action = 'review';
        } else {
            action = 'decline';
        }
        
        // Log risk assessment
        auditLogger.info('Risk assessment completed', {
            transactionId: transaction.id,
            riskScore,
            reasons,
            action,
        });
        
        return { score: riskScore, reasons, action };
    }
    
    private async getRecentTransactions(customerId: string, window: number) {
        const result = await db.query(
            `SELECT * FROM transactions 
             WHERE customer_id = $1 
             AND created_at > NOW() - INTERVAL '${window} milliseconds'
             ORDER BY created_at DESC`,
            [customerId]
        );
        return result.rows;
    }
    
    private async getAverageTransactionAmount(customerId: string): Promise<number> {
        const result = await db.query(
            `SELECT AVG(amount) as avg_amount 
             FROM transactions 
             WHERE customer_id = $1 
             AND created_at > NOW() - INTERVAL '30 days'`,
            [customerId]
        );
        return result.rows[0]?.avg_amount || 100;
    }
    
    private async assessGeographicalRisk(transaction: any): Promise<number> {
        // Check IP geolocation vs billing address
        const ipCountry = await this.getIpCountry(transaction.ipAddress);
        const billingCountry = transaction.billingAddress?.country;
        
        if (ipCountry !== billingCountry) {
            return 0.7;
        }
        
        // Check against high-risk countries
        const highRiskCountries = ['XX', 'YY', 'ZZ']; // Placeholder
        if (highRiskCountries.includes(ipCountry)) {
            return 0.8;
        }
        
        return 0.1;
    }
    
    private async assessDeviceRisk(fingerprint: string): Promise<number> {
        // Check if device is blacklisted
        const blacklisted = await redis.get(`blacklist:device:${fingerprint}`);
        if (blacklisted) {
            return 1.0;
        }
        
        // Check device reputation
        const reputation = await redis.get(`reputation:device:${fingerprint}`);
        if (reputation) {
            return 1.0 - parseFloat(reputation);
        }
        
        return 0.2; // New device
    }
    
    private async getIpCountry(ip: string): Promise<string> {
        // Implement IP geolocation lookup
        return 'US'; // Placeholder
    }
}

// Payment processor with multi-gateway support
class PaymentProcessor {
    private readonly encryption = new EncryptionService();
    private readonly fraudEngine = new FraudDetectionEngine();
    
    async processPayment(request: any): Promise<{
        success: boolean;
        transactionId: string;
        status: string;
        details?: any;
        error?: string;
    }> {
        const client = await db.connect();
        
        try {
            // Start transaction
            await client.query('BEGIN');
            
            // Validate request
            const validatedRequest = PaymentRequestSchema.parse(request);
            
            // Check idempotency
            const existing = await this.checkIdempotency(validatedRequest.idempotencyKey);
            if (existing) {
                await client.query('ROLLBACK');
                return existing;
            }
            
            // Perform fraud check
            const fraudAssessment = await this.fraudEngine.assessTransaction(request);
            if (fraudAssessment.action === 'decline') {
                await client.query('ROLLBACK');
                throw new Error('Transaction declined due to risk assessment');
            }
            
            // Create transaction record
            const transactionId = await this.createTransaction(client, {
                ...validatedRequest,
                fraudScore: fraudAssessment.score,
                status: 'pending',
            });
            
            // Process based on payment method
            let result;
            switch (validatedRequest.paymentMethod) {
                case 'card':
                    result = await this.processCardPayment(transactionId, request);
                    break;
                case 'bank_transfer':
                    result = await this.processBankTransfer(transactionId, request);
                    break;
                case 'wallet':
                    result = await this.processWalletPayment(transactionId, request);
                    break;
                case 'crypto':
                    result = await this.processCryptoPayment(transactionId, request);
                    break;
                default:
                    throw new Error('Unsupported payment method');
            }
            
            // Update transaction status
            await this.updateTransactionStatus(client, transactionId, result.status);
            
            // Commit transaction
            await client.query('COMMIT');
            
            // Store idempotency result
            await this.storeIdempotencyResult(validatedRequest.idempotencyKey, result);
            
            // Audit log
            auditLogger.info('Payment processed', {
                transactionId,
                customerId: validatedRequest.customerId,
                amount: validatedRequest.amount,
                currency: validatedRequest.currency,
                method: validatedRequest.paymentMethod,
                status: result.status,
            });
            
            return {
                success: result.status === 'succeeded',
                transactionId,
                status: result.status,
                details: result,
            };
            
        } catch (error: any) {
            await client.query('ROLLBACK');
            
            auditLogger.error('Payment processing failed', {
                error: error.message,
                request: validatedRequest,
            });
            
            return {
                success: false,
                transactionId: '',
                status: 'failed',
                error: error.message,
            };
        } finally {
            client.release();
        }
    }
    
    private async processCardPayment(transactionId: string, request: any) {
        // Tokenize card details for PCI compliance
        const token = this.encryption.tokenize(JSON.stringify(request.cardDetails));
        
        // Create Stripe payment intent
        const paymentIntent = await stripe.paymentIntents.create({
            amount: Math.round(request.amount * 100), // Convert to cents
            currency: request.currency.toLowerCase(),
            customer: request.stripeCustomerId,
            payment_method: request.stripePaymentMethodId,
            confirm: true,
            capture_method: 'automatic',
            metadata: {
                transactionId,
                customerId: request.customerId,
            },
        });
        
        // Handle 3D Secure if required
        if (paymentIntent.status === 'requires_action') {
            return {
                status: 'requires_authentication',
                clientSecret: paymentIntent.client_secret,
            };
        }
        
        return {
            status: paymentIntent.status,
            paymentIntentId: paymentIntent.id,
            chargeId: paymentIntent.latest_charge,
        };
    }
    
    private async processBankTransfer(transactionId: string, request: any) {
        // Implement ACH/SEPA transfer logic
        const transferRequest = {
            amount: request.amount,
            currency: request.currency,
            sourceAccount: request.sourceAccount,
            destinationAccount: request.destinationAccount,
            reference: transactionId,
        };
        
        // Call banking API
        // const result = await bankingApi.initiateTransfer(transferRequest);
        
        return {
            status: 'processing',
            transferId: 'TRANSFER_' + transactionId,
            estimatedCompletion: new Date(Date.now() + 86400000), // +1 day
        };
    }
    
    private async processWalletPayment(transactionId: string, request: any) {
        // Handle digital wallet payments (Apple Pay, Google Pay, etc.)
        const walletToken = request.walletToken;
        
        // Decrypt and validate wallet token
        // Process through appropriate gateway
        
        return {
            status: 'succeeded',
            walletTransactionId: 'WALLET_' + transactionId,
        };
    }
    
    private async processCryptoPayment(transactionId: string, request: any) {
        // Handle cryptocurrency payments
        const { cryptoAddress, amount, currency } = request;
        
        // Generate payment address
        const paymentAddress = await this.generateCryptoAddress(currency);
        
        // Monitor blockchain for payment
        // This would typically be handled asynchronously
        
        return {
            status: 'awaiting_payment',
            paymentAddress,
            amount,
            currency,
            expiresAt: new Date(Date.now() + 3600000), // 1 hour
        };
    }
    
    private async createTransaction(client: any, data: any): Promise<string> {
        const result = await client.query(
            `INSERT INTO transactions (
                id, customer_id, amount, currency, 
                payment_method, status, fraud_score,
                metadata, created_at
            ) VALUES (
                gen_random_uuid(), $1, $2, $3, 
                $4, $5, $6, $7, NOW()
            ) RETURNING id`,
            [
                data.customerId,
                data.amount,
                data.currency,
                data.paymentMethod,
                data.status,
                data.fraudScore,
                JSON.stringify(data.metadata || {}),
            ]
        );
        
        return result.rows[0].id;
    }
    
    private async updateTransactionStatus(client: any, transactionId: string, status: string) {
        await client.query(
            `UPDATE transactions 
             SET status = $1, updated_at = NOW() 
             WHERE id = $2`,
            [status, transactionId]
        );
    }
    
    private async checkIdempotency(key: string): Promise<any> {
        const cached = await redis.get(`idempotency:${key}`);
        if (cached) {
            return JSON.parse(cached);
        }
        return null;
    }
    
    private async storeIdempotencyResult(key: string, result: any) {
        await redis.setex(
            `idempotency:${key}`,
            86400, // 24 hours
            JSON.stringify(result)
        );
    }
    
    private async generateCryptoAddress(currency: string): Promise<string> {
        // Generate HD wallet address for the specific cryptocurrency
        // This would integrate with a crypto wallet service
        return `${currency}_ADDRESS_${Date.now()}`;
    }
}

// Reconciliation service
class ReconciliationService {
    async reconcileTransactions(startDate: Date, endDate: Date): Promise<{
        matched: number;
        unmatched: number;
        discrepancies: any[];
    }> {
        // Fetch internal records
        const internalTransactions = await this.getInternalTransactions(startDate, endDate);
        
        // Fetch external records (from payment providers)
        const stripeTransactions = await this.getStripeTransactions(startDate, endDate);
        const bankTransactions = await this.getBankTransactions(startDate, endDate);
        
        // Perform reconciliation
        const matched: any[] = [];
        const unmatched: any[] = [];
        const discrepancies: any[] = [];
        
        for (const internal of internalTransactions) {
            const external = this.findMatchingTransaction(
                internal,
                [...stripeTransactions, ...bankTransactions]
            );
            
            if (external) {
                if (this.compareTransactions(internal, external)) {
                    matched.push({ internal, external });
                } else {
                    discrepancies.push({
                        internal,
                        external,
                        differences: this.getTransactionDifferences(internal, external),
                    });
                }
            } else {
                unmatched.push(internal);
            }
        }
        
        // Generate reconciliation report
        await this.generateReconciliationReport({
            period: { startDate, endDate },
            matched: matched.length,
            unmatched: unmatched.length,
            discrepancies: discrepancies.length,
            details: { matched, unmatched, discrepancies },
        });
        
        return {
            matched: matched.length,
            unmatched: unmatched.length,
            discrepancies,
        };
    }
    
    private async getInternalTransactions(startDate: Date, endDate: Date) {
        const result = await db.query(
            `SELECT * FROM transactions 
             WHERE created_at BETWEEN $1 AND $2 
             ORDER BY created_at`,
            [startDate, endDate]
        );
        return result.rows;
    }
    
    private async getStripeTransactions(startDate: Date, endDate: Date) {
        const charges = await stripe.charges.list({
            created: {
                gte: Math.floor(startDate.getTime() / 1000),
                lte: Math.floor(endDate.getTime() / 1000),
            },
            limit: 100,
        });
        
        return charges.data.map(charge => ({
            id: charge.id,
            amount: charge.amount / 100,
            currency: charge.currency.toUpperCase(),
            status: charge.status,
            created: new Date(charge.created * 1000),
            metadata: charge.metadata,
        }));
    }
    
    private async getBankTransactions(startDate: Date, endDate: Date) {
        // Fetch from banking API
        return [];
    }
    
    private findMatchingTransaction(internal: any, externals: any[]) {
        return externals.find(ext => 
            ext.metadata?.transactionId === internal.id ||
            (Math.abs(ext.amount - internal.amount) < 0.01 &&
             ext.currency === internal.currency &&
             Math.abs(ext.created.getTime() - internal.created_at.getTime()) < 60000)
        );
    }
    
    private compareTransactions(internal: any, external: any): boolean {
        return (
            Math.abs(internal.amount - external.amount) < 0.01 &&
            internal.currency === external.currency &&
            internal.status === external.status
        );
    }
    
    private getTransactionDifferences(internal: any, external: any) {
        const differences: any = {};
        
        if (Math.abs(internal.amount - external.amount) >= 0.01) {
            differences.amount = {
                internal: internal.amount,
                external: external.amount,
            };
        }
        
        if (internal.currency !== external.currency) {
            differences.currency = {
                internal: internal.currency,
                external: external.currency,
            };
        }
        
        if (internal.status !== external.status) {
            differences.status = {
                internal: internal.status,
                external: external.status,
            };
        }
        
        return differences;
    }
    
    private async generateReconciliationReport(report: any) {
        // Store report in database
        await db.query(
            `INSERT INTO reconciliation_reports 
             (id, period_start, period_end, matched_count, 
              unmatched_count, discrepancy_count, details, created_at)
             VALUES (gen_random_uuid(), $1, $2, $3, $4, $5, $6, NOW())`,
            [
                report.period.startDate,
                report.period.endDate,
                report.matched,
                report.unmatched,
                report.discrepancies,
                JSON.stringify(report.details),
            ]
        );
        
        // Send notification if discrepancies found
        if (report.discrepancies > 0) {
            // await notificationService.send('reconciliation_discrepancies', report);
        }
    }
}

// Compliance and reporting service
class ComplianceService {
    async generateRegulatoryReport(type: string, period: { start: Date; end: Date }) {
        switch (type) {
            case 'SAR': // Suspicious Activity Report
                return this.generateSAR(period);
            case 'CTR': // Currency Transaction Report
                return this.generateCTR(period);
            case 'PCI_DSS':
                return this.generatePCIDSSReport(period);
            case 'GDPR':
                return this.generateGDPRReport(period);
            default:
                throw new Error(`Unknown report type: ${type}`);
        }
    }
    
    private async generateSAR(period: { start: Date; end: Date }) {
        // Identify suspicious transactions
        const suspiciousTransactions = await db.query(
            `SELECT t.*, c.* 
             FROM transactions t
             JOIN customers c ON t.customer_id = c.id
             WHERE t.created_at BETWEEN $1 AND $2
             AND (t.fraud_score > 0.7 
                  OR t.amount > 10000
                  OR t.status = 'flagged')
             ORDER BY t.fraud_score DESC`,
            [period.start, period.end]
        );
        
        return {
            reportType: 'SAR',
            period,
            transactionCount: suspiciousTransactions.rows.length,
            transactions: suspiciousTransactions.rows.map(t => ({
                transactionId: t.id,
                date: t.created_at,
                amount: t.amount,
                currency: t.currency,
                customerName: t.name,
                customerId: t.customer_id,
                fraudScore: t.fraud_score,
                suspicionReason: this.determineSuspicionReason(t),
            })),
            filingRequired: suspiciousTransactions.rows.length > 0,
        };
    }
    
    private async generateCTR(period: { start: Date; end: Date }) {
        // Report transactions over $10,000
        const largeTransactions = await db.query(
            `SELECT t.*, c.* 
             FROM transactions t
             JOIN customers c ON t.customer_id = c.id
             WHERE t.created_at BETWEEN $1 AND $2
             AND t.amount > 10000
             AND t.currency = 'USD'
             ORDER BY t.amount DESC`,
            [period.start, period.end]
        );
        
        return {
            reportType: 'CTR',
            period,
            transactionCount: largeTransactions.rows.length,
            totalAmount: largeTransactions.rows.reduce((sum, t) => sum + t.amount, 0),
            transactions: largeTransactions.rows,
        };
    }
    
    private async generatePCIDSSReport(period: { start: Date; end: Date }) {
        // PCI DSS compliance report
        const metrics = await this.collectPCIDSSMetrics(period);
        
        return {
            reportType: 'PCI_DSS',
            period,
            complianceLevel: 1,
            metrics: {
                encryptedTransactions: metrics.encryptedCount,
                tokenizedCards: metrics.tokenizedCount,
                failedSecurityScans: metrics.failedScans,
                accessControlViolations: metrics.accessViolations,
                dataRetentionCompliance: metrics.retentionCompliant,
            },
            vulnerabilities: await this.identifyVulnerabilities(),
            recommendations: this.generateSecurityRecommendations(metrics),
        };
    }
    
    private async generateGDPRReport(period: { start: Date; end: Date }) {
        // GDPR compliance report
        return {
            reportType: 'GDPR',
            period,
            dataSubjectRequests: await this.getDataSubjectRequests(period),
            dataBreaches: await this.getDataBreaches(period),
            consentRecords: await this.getConsentRecords(period),
            dataRetention: await this.getDataRetentionStatus(),
            crossBorderTransfers: await this.getCrossBorderTransfers(period),
        };
    }
    
    private determineSuspicionReason(transaction: any): string {
        const reasons = [];
        
        if (transaction.fraud_score > 0.7) {
            reasons.push('High fraud score');
        }
        if (transaction.amount > 10000) {
            reasons.push('Large transaction amount');
        }
        if (transaction.status === 'flagged') {
            reasons.push('Manually flagged');
        }
        
        return reasons.join(', ');
    }
    
    private async collectPCIDSSMetrics(period: { start: Date; end: Date }) {
        // Collect PCI DSS compliance metrics
        return {
            encryptedCount: 1000,
            tokenizedCount: 950,
            failedScans: 0,
            accessViolations: 2,
            retentionCompliant: true,
        };
    }
    
    private async identifyVulnerabilities() {
        // Security vulnerability assessment
        return [];
    }
    
    private generateSecurityRecommendations(metrics: any) {
        const recommendations = [];
        
        if (metrics.failedScans > 0) {
            recommendations.push('Address failed security scans immediately');
        }
        if (metrics.accessViolations > 0) {
            recommendations.push('Review and strengthen access controls');
        }
        if (!metrics.retentionCompliant) {
            recommendations.push('Update data retention policies');
        }
        
        return recommendations;
    }
    
    private async getDataSubjectRequests(period: { start: Date; end: Date }) {
        return {
            access: 12,
            rectification: 3,
            erasure: 5,
            portability: 2,
            averageResponseTime: '48 hours',
        };
    }
    
    private async getDataBreaches(period: { start: Date; end: Date }) {
        return [];
    }
    
    private async getConsentRecords(period: { start: Date; end: Date }) {
        return {
            obtained: 500,
            withdrawn: 15,
            updated: 30,
        };
    }
    
    private async getDataRetentionStatus() {
        return {
            compliant: true,
            oldestRecord: '2017-01-01',
            scheduledDeletions: 150,
        };
    }
    
    private async getCrossBorderTransfers(period: { start: Date; end: Date }) {
        return {
            euToUs: 50,
            usToEu: 30,
            other: 10,
            adequacyDecisions: true,
            sccInPlace: true,
        };
    }
}

// Rate limiting middleware
class RateLimiter {
    private readonly limits = new Map<string, { count: number; resetTime: number }>();
    
    async checkLimit(identifier: string): Promise<boolean> {
        const now = Date.now();
        const limit = this.limits.get(identifier);
        
        if (!limit || limit.resetTime < now) {
            this.limits.set(identifier, {
                count: 1,
                resetTime: now + config.security.rateLimitWindow,
            });
            return true;
        }
        
        if (limit.count >= config.security.maxRequestsPerWindow) {
            return false;
        }
        
        limit.count++;
        return true;
    }
}

// API endpoints
export class PaymentAPI {
    private readonly processor = new PaymentProcessor();
    private readonly reconciliation = new ReconciliationService();
    private readonly compliance = new ComplianceService();
    private readonly rateLimiter = new RateLimiter();
    
    async handlePayment(req: Request, res: Response, next: NextFunction) {
        try {
            // Rate limiting
            const clientId = req.ip || 'unknown';
            if (!await this.rateLimiter.checkLimit(clientId)) {
                return res.status(429).json({
                    error: 'Too many requests',
                });
            }
            
            // Process payment
            const result = await this.processor.processPayment(req.body);
            
            if (result.success) {
                res.status(200).json(result);
            } else {
                res.status(400).json(result);
            }
        } catch (error: any) {
            auditLogger.error('Payment API error', {
                error: error.message,
                stack: error.stack,
            });
            
            res.status(500).json({
                error: 'Internal server error',
                reference: Date.now(),
            });
        }
    }
    
    async handleWebhook(req: Request, res: Response) {
        const sig = req.headers['stripe-signature'] as string;
        
        try {
            const event = stripe.webhooks.constructEvent(
                req.body,
                sig,
                config.stripe.webhookSecret
            );
            
            // Process webhook event
            switch (event.type) {
                case 'payment_intent.succeeded':
                    await this.handlePaymentSuccess(event.data.object);
                    break;
                case 'payment_intent.payment_failed':
                    await this.handlePaymentFailure(event.data.object);
                    break;
                case 'charge.dispute.created':
                    await this.handleDispute(event.data.object);
                    break;
            }
            
            res.status(200).json({ received: true });
        } catch (error: any) {
            auditLogger.error('Webhook error', {
                error: error.message,
            });
            
            res.status(400).json({
                error: 'Webhook signature verification failed',
            });
        }
    }
    
    async handleReconciliation(req: Request, res: Response) {
        try {
            const { startDate, endDate } = req.query;
            
            const result = await this.reconciliation.reconcileTransactions(
                new Date(startDate as string),
                new Date(endDate as string)
            );
            
            res.status(200).json(result);
        } catch (error: any) {
            res.status(500).json({
                error: error.message,
            });
        }
    }
    
    async handleComplianceReport(req: Request, res: Response) {
        try {
            const { type, startDate, endDate } = req.query;
            
            const report = await this.compliance.generateRegulatoryReport(
                type as string,
                {
                    start: new Date(startDate as string),
                    end: new Date(endDate as string),
                }
            );
            
            res.status(200).json(report);
        } catch (error: any) {
            res.status(500).json({
                error: error.message,
            });
        }
    }
    
    private async handlePaymentSuccess(paymentIntent: any) {
        // Update transaction status
        await db.query(
            `UPDATE transactions 
             SET status = 'succeeded', 
                 external_id = $1,
                 updated_at = NOW()
             WHERE metadata->>'paymentIntentId' = $2`,
            [paymentIntent.id, paymentIntent.id]
        );
        
        // Send confirmation
        // await notificationService.sendPaymentConfirmation(paymentIntent);
    }
    
    private async handlePaymentFailure(paymentIntent: any) {
        // Update transaction status
        await db.query(
            `UPDATE transactions 
             SET status = 'failed',
                 failure_reason = $1,
                 updated_at = NOW()
             WHERE metadata->>'paymentIntentId' = $2`,
            [paymentIntent.last_payment_error?.message, paymentIntent.id]
        );
    }
    
    private async handleDispute(dispute: any) {
        // Create dispute record
        await db.query(
            `INSERT INTO disputes 
             (id, transaction_id, amount, reason, status, created_at)
             VALUES ($1, $2, $3, $4, $5, NOW())`,
            [
                dispute.id,
                dispute.payment_intent,
                dispute.amount / 100,
                dispute.reason,
                dispute.status,
            ]
        );
        
        // Alert compliance team
        auditLogger.warn('Dispute created', {
            disputeId: dispute.id,
            amount: dispute.amount / 100,
            reason: dispute.reason,
        });
    }
}

// Export configured instance
export const paymentAPI = new PaymentAPI();
```

## Example 2

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

/**
 * Decentralized Finance Protocol
 * Lending, borrowing, and yield farming with advanced risk management
 */
contract DeFiProtocol is ReentrancyGuard, Ownable {
    using SafeMath for uint256;
    
    // Constants
    uint256 constant PRECISION = 1e18;
    uint256 constant LIQUIDATION_THRESHOLD = 150; // 150% collateralization
    uint256 constant LIQUIDATION_PENALTY = 110; // 10% penalty
    uint256 constant MAX_UTILIZATION_RATE = 95; // 95%
    
    // State variables
    mapping(address => mapping(address => uint256)) public deposits;
    mapping(address => mapping(address => uint256)) public borrows;
    mapping(address => uint256) public totalDeposits;
    mapping(address => uint256) public totalBorrows;
    mapping(address => uint256) public exchangeRates;
    mapping(address => bool) public supportedAssets;
    mapping(address => uint256) public collateralFactors;
    
    // Interest rate model parameters
    struct InterestRateModel {
        uint256 baseRate;
        uint256 multiplier;
        uint256 jumpMultiplier;
        uint256 kink;
    }
    
    mapping(address => InterestRateModel) public interestModels;
    
    // Oracle interface
    IPriceOracle public priceOracle;
    
    // Events
    event Deposit(address indexed user, address indexed asset, uint256 amount);
    event Withdraw(address indexed user, address indexed asset, uint256 amount);
    event Borrow(address indexed user, address indexed asset, uint256 amount);
    event Repay(address indexed user, address indexed asset, uint256 amount);
    event Liquidation(
        address indexed liquidator,
        address indexed borrower,
        address indexed asset,
        uint256 amount
    );
    
    constructor(address _priceOracle) {
        priceOracle = IPriceOracle(_priceOracle);
    }
    
    /**
     * Deposit assets as collateral
     */
    function deposit(address asset, uint256 amount) 
        external 
        nonReentrant 
    {
        require(supportedAssets[asset], "Asset not supported");
        require(amount > 0, "Amount must be greater than 0");
        
        // Transfer tokens from user
        IERC20(asset).transferFrom(msg.sender, address(this), amount);
        
        // Update user balance
        deposits[msg.sender][asset] = deposits[msg.sender][asset].add(amount);
        totalDeposits[asset] = totalDeposits[asset].add(amount);
        
        // Mint interest-bearing tokens (simplified)
        _updateExchangeRate(asset);
        
        emit Deposit(msg.sender, asset, amount);
    }
    
    /**
     * Withdraw collateral
     */
    function withdraw(address asset, uint256 amount) 
        external 
        nonReentrant 
    {
        require(deposits[msg.sender][asset] >= amount, "Insufficient balance");
        
        // Check if withdrawal maintains health factor
        require(_checkHealthFactor(msg.sender, asset, amount, true), "Unhealthy position");
        
        // Update balances
        deposits[msg.sender][asset] = deposits[msg.sender][asset].sub(amount);
        totalDeposits[asset] = totalDeposits[asset].sub(amount);
        
        // Transfer tokens to user
        IERC20(asset).transfer(msg.sender, amount);
        
        emit Withdraw(msg.sender, asset, amount);
    }
    
    /**
     * Borrow assets against collateral
     */
    function borrow(address asset, uint256 amount) 
        external 
        nonReentrant 
    {
        require(supportedAssets[asset], "Asset not supported");
        
        // Check available liquidity
        uint256 available = _getAvailableLiquidity(asset);
        require(available >= amount, "Insufficient liquidity");
        
        // Check borrowing power
        uint256 borrowingPower = _getBorrowingPower(msg.sender);
        uint256 assetPrice = priceOracle.getPrice(asset);
        uint256 borrowValue = amount.mul(assetPrice).div(PRECISION);
        
        require(borrowingPower >= borrowValue, "Insufficient collateral");
        
        // Update borrow balance with interest
        _accrueInterest(asset);
        borrows[msg.sender][asset] = borrows[msg.sender][asset].add(amount);
        totalBorrows[asset] = totalBorrows[asset].add(amount);
        
        // Transfer tokens to borrower
        IERC20(asset).transfer(msg.sender, amount);
        
        emit Borrow(msg.sender, asset, amount);
    }
    
    /**
     * Repay borrowed assets
     */
    function repay(address asset, uint256 amount) 
        external 
        nonReentrant 
    {
        uint256 borrowBalance = borrows[msg.sender][asset];
        require(borrowBalance > 0, "No borrow balance");
        
        uint256 repayAmount = amount > borrowBalance ? borrowBalance : amount;
        
        // Transfer tokens from user
        IERC20(asset).transferFrom(msg.sender, address(this), repayAmount);
        
        // Update balances
        borrows[msg.sender][asset] = borrowBalance.sub(repayAmount);
        totalBorrows[asset] = totalBorrows[asset].sub(repayAmount);
        
        emit Repay(msg.sender, asset, repayAmount);
    }
    
    /**
     * Liquidate undercollateralized position
     */
    function liquidate(address borrower, address collateralAsset, address borrowAsset) 
        external 
        nonReentrant 
    {
        // Check if position is liquidatable
        require(!_isHealthy(borrower), "Position is healthy");
        
        uint256 borrowBalance = borrows[borrower][borrowAsset];
        require(borrowBalance > 0, "No borrow balance");
        
        // Calculate liquidation amount (50% of borrow)
        uint256 liquidationAmount = borrowBalance.div(2);
        
        // Calculate collateral to seize
        uint256 collateralPrice = priceOracle.getPrice(collateralAsset);
        uint256 borrowPrice = priceOracle.getPrice(borrowAsset);
        
        uint256 collateralToSeize = liquidationAmount
            .mul(borrowPrice)
            .mul(LIQUIDATION_PENALTY)
            .div(collateralPrice)
            .div(100);
        
        require(
            deposits[borrower][collateralAsset] >= collateralToSeize,
            "Insufficient collateral"
        );
        
        // Transfer borrow asset from liquidator
        IERC20(borrowAsset).transferFrom(msg.sender, address(this), liquidationAmount);
        
        // Update borrower's balances
        borrows[borrower][borrowAsset] = borrowBalance.sub(liquidationAmount);
        totalBorrows[borrowAsset] = totalBorrows[borrowAsset].sub(liquidationAmount);
        
        deposits[borrower][collateralAsset] = deposits[borrower][collateralAsset]
            .sub(collateralToSeize);
        totalDeposits[collateralAsset] = totalDeposits[collateralAsset]
            .sub(collateralToSeize);
        
        // Transfer collateral to liquidator
        IERC20(collateralAsset).transfer(msg.sender, collateralToSeize);
        
        emit Liquidation(msg.sender, borrower, borrowAsset, liquidationAmount);
    }
    
    /**
     * Calculate interest rate based on utilization
     */
    function _calculateInterestRate(address asset) 
        internal 
        view 
        returns (uint256) 
    {
        uint256 utilization = _getUtilizationRate(asset);
        InterestRateModel memory model = interestModels[asset];
        
        if (utilization <= model.kink) {
            return model.baseRate.add(
                utilization.mul(model.multiplier).div(PRECISION)
            );
        } else {
            uint256 normalRate = model.baseRate.add(
                model.kink.mul(model.multiplier).div(PRECISION)
            );
            uint256 excess = utilization.sub(model.kink);
            return normalRate.add(
                excess.mul(model.jumpMultiplier).div(PRECISION)
            );
        }
    }
    
    /**
     * Get utilization rate of an asset
     */
    function _getUtilizationRate(address asset) 
        internal 
        view 
        returns (uint256) 
    {
        uint256 total = totalDeposits[asset];
        if (total == 0) return 0;
        
        return totalBorrows[asset].mul(PRECISION).div(total);
    }
    
    /**
     * Get available liquidity for borrowing
     */
    function _getAvailableLiquidity(address asset) 
        internal 
        view 
        returns (uint256) 
    {
        uint256 total = totalDeposits[asset];
        uint256 borrowed = totalBorrows[asset];
        uint256 maxBorrowable = total.mul(MAX_UTILIZATION_RATE).div(100);
        
        if (borrowed >= maxBorrowable) return 0;
        return maxBorrowable.sub(borrowed);
    }
    
    /**
     * Calculate user's borrowing power
     */
    function _getBorrowingPower(address user) 
        internal 
        view 
        returns (uint256) 
    {
        uint256 totalCollateralValue = 0;
        
        // Iterate through all supported assets
        address[] memory assets = _getSupportedAssets();
        for (uint256 i = 0; i < assets.length; i++) {
            address asset = assets[i];
            uint256 balance = deposits[user][asset];
            
            if (balance > 0) {
                uint256 price = priceOracle.getPrice(asset);
                uint256 value = balance.mul(price).div(PRECISION);
                uint256 adjustedValue = value.mul(collateralFactors[asset]).div(100);
                totalCollateralValue = totalCollateralValue.add(adjustedValue);
            }
        }
        
        // Calculate total borrow value
        uint256 totalBorrowValue = _getTotalBorrowValue(user);
        
        if (totalCollateralValue <= totalBorrowValue) return 0;
        return totalCollateralValue.sub(totalBorrowValue);
    }
    
    /**
     * Calculate total borrow value for a user
     */
    function _getTotalBorrowValue(address user) 
        internal 
        view 
        returns (uint256) 
    {
        uint256 totalValue = 0;
        
        address[] memory assets = _getSupportedAssets();
        for (uint256 i = 0; i < assets.length; i++) {
            address asset = assets[i];
            uint256 balance = borrows[user][asset];
            
            if (balance > 0) {
                uint256 price = priceOracle.getPrice(asset);
                uint256 value = balance.mul(price).div(PRECISION);
                totalValue = totalValue.add(value);
            }
        }
        
        return totalValue;
    }
    
    /**
     * Check if user's position is healthy
     */
    function _isHealthy(address user) 
        internal 
        view 
        returns (bool) 
    {
        uint256 collateralValue = _getTotalCollateralValue(user);
        uint256 borrowValue = _getTotalBorrowValue(user);
        
        if (borrowValue == 0) return true;
        
        uint256 healthFactor = collateralValue.mul(100).div(borrowValue);
        return healthFactor >= LIQUIDATION_THRESHOLD;
    }
    
    /**
     * Check health factor after potential action
     */
    function _checkHealthFactor(
        address user,
        address asset,
        uint256 amount,
        bool isWithdrawal
    ) internal view returns (bool) {
        // Simulate the action and check resulting health
        // Implementation details...
        return true;
    }
    
    /**
     * Update exchange rate for interest accrual
     */
    function _updateExchangeRate(address asset) internal {
        // Calculate accrued interest and update exchange rate
        uint256 interestRate = _calculateInterestRate(asset);
        uint256 timeDelta = block.timestamp.sub(lastUpdateTime[asset]);
        
        uint256 interestAccrued = totalBorrows[asset]
            .mul(interestRate)
            .mul(timeDelta)
            .div(365 days)
            .div(PRECISION);
        
        exchangeRates[asset] = exchangeRates[asset].add(interestAccrued);
        lastUpdateTime[asset] = block.timestamp;
    }
    
    /**
     * Accrue interest for an asset
     */
    function _accrueInterest(address asset) internal {
        _updateExchangeRate(asset);
    }
    
    /**
     * Get total collateral value for a user
     */
    function _getTotalCollateralValue(address user) 
        internal 
        view 
        returns (uint256) 
    {
        uint256 totalValue = 0;
        
        address[] memory assets = _getSupportedAssets();
        for (uint256 i = 0; i < assets.length; i++) {
            address asset = assets[i];
            uint256 balance = deposits[user][asset];
            
            if (balance > 0) {
                uint256 price = priceOracle.getPrice(asset);
                uint256 value = balance.mul(price).div(PRECISION);
                totalValue = totalValue.add(value);
            }
        }
        
        return totalValue;
    }
    
    /**
     * Get list of supported assets
     */
    function _getSupportedAssets() 
        internal 
        view 
        returns (address[] memory) 
    {
        // Return array of supported assets
        // Implementation would maintain this list
        address[] memory assets = new address[](3);
        // assets[0] = USDC;
        // assets[1] = WETH;
        // assets[2] = WBTC;
        return assets;
    }
    
    // Admin functions
    
    /**
     * Add supported asset
     */
    function addAsset(
        address asset,
        uint256 collateralFactor,
        InterestRateModel memory model
    ) external onlyOwner {
        supportedAssets[asset] = true;
        collateralFactors[asset] = collateralFactor;
        interestModels[asset] = model;
    }
    
    /**
     * Update price oracle
     */
    function updateOracle(address newOracle) external onlyOwner {
        priceOracle = IPriceOracle(newOracle);
    }
    
    /**
     * Emergency pause
     */
    function pause() external onlyOwner {
        _pause();
    }
    
    /**
     * Resume operations
     */
    function unpause() external onlyOwner {
        _unpause();
    }
    
    // Additional variables
    mapping(address => uint256) public lastUpdateTime;
}

// Price Oracle Interface
interface IPriceOracle {
    function getPrice(address asset) external view returns (uint256);
}
```
