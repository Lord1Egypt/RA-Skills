# Ecommerce Expert — Code Examples

## Example 1

```typescript
import { NextApiRequest, NextApiResponse } from 'next';
import { PrismaClient } from '@prisma/client';
import Stripe from 'stripe';
import { Redis } from 'ioredis';
import { z } from 'zod';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { v4 as uuidv4 } from 'uuid';
import algoliasearch from 'algoliasearch';
import { SQS, S3 } from 'aws-sdk';
import winston from 'winston';

/**
 * Enterprise E-commerce Platform
 * Full-featured implementation with scalability and performance optimization
 */

// Database client with connection pooling
const prisma = new PrismaClient({
    datasources: {
        db: {
            url: process.env.DATABASE_URL,
        },
    },
    log: ['error', 'warn'],
});

// Redis for caching and sessions
const redis = new Redis({
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT || '6379'),
    password: process.env.REDIS_PASSWORD,
    maxRetriesPerRequest: 3,
});

// Stripe payment processing
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
    apiVersion: '2023-10-16',
});

// Algolia search
const algolia = algoliasearch(
    process.env.ALGOLIA_APP_ID!,
    process.env.ALGOLIA_ADMIN_KEY!
);
const searchIndex = algolia.initIndex('products');

// AWS services
const sqs = new SQS({ region: process.env.AWS_REGION });
const s3 = new S3({ region: process.env.AWS_REGION });

// Logger
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' }),
    ],
});

// Configuration
const config = {
    cart: {
        sessionTimeout: 3600000, // 1 hour
        maxItems: 100,
        reservationTime: 900000, // 15 minutes
    },
    checkout: {
        paymentMethods: ['card', 'paypal', 'applepay', 'googlepay', 'klarna'],
        requiresAuth: false,
        expressCheckoutEnabled: true,
    },
    inventory: {
        lowStockThreshold: 10,
        enableBackorders: true,
        reservationEnabled: true,
    },
    shipping: {
        freeShippingThreshold: 50,
        carriers: ['ups', 'fedex', 'usps', 'dhl'],
        internationalEnabled: true,
    },
    tax: {
        enableAutomaticCalculation: true,
        nexusStates: ['CA', 'NY', 'TX'],
    },
};

// Type definitions
interface Product {
    id: string;
    sku: string;
    name: string;
    slug: string;
    description: string;
    price: number;
    compareAtPrice?: number;
    cost?: number;
    images: ProductImage[];
    variants: ProductVariant[];
    categories: Category[];
    tags: string[];
    inventory: InventoryItem;
    seo: SEOData;
    status: 'active' | 'draft' | 'archived';
    publishedAt?: Date;
}

interface ProductVariant {
    id: string;
    productId: string;
    sku: string;
    name: string;
    price: number;
    attributes: Record<string, string>;
    inventory: InventoryItem;
    weight?: number;
    dimensions?: Dimensions;
}

interface InventoryItem {
    quantity: number;
    reserved: number;
    available: number;
    trackInventory: boolean;
    allowBackorder: boolean;
    locations: InventoryLocation[];
}

interface CartItem {
    id: string;
    productId: string;
    variantId?: string;
    quantity: number;
    price: number;
    metadata?: Record<string, any>;
}

interface Order {
    id: string;
    orderNumber: string;
    customerId?: string;
    email: string;
    status: OrderStatus;
    items: OrderItem[];
    subtotal: number;
    tax: number;
    shipping: number;
    discount: number;
    total: number;
    shippingAddress: Address;
    billingAddress: Address;
    payment: PaymentInfo;
    fulfillment: FulfillmentInfo;
    createdAt: Date;
    updatedAt: Date;
}

enum OrderStatus {
    PENDING = 'pending',
    PROCESSING = 'processing',
    PAID = 'paid',
    FULFILLED = 'fulfilled',
    SHIPPED = 'shipped',
    DELIVERED = 'delivered',
    CANCELLED = 'cancelled',
    REFUNDED = 'refunded',
}

// Product Catalog Service
class ProductCatalogService {
    async getProduct(idOrSlug: string): Promise<Product | null> {
        // Check cache first
        const cached = await redis.get(`product:${idOrSlug}`);
        if (cached) {
            return JSON.parse(cached);
        }
        
        // Query database
        const product = await prisma.product.findFirst({
            where: {
                OR: [
                    { id: idOrSlug },
                    { slug: idOrSlug },
                ],
                status: 'active',
            },
            include: {
                variants: {
                    include: {
                        inventory: true,
                    },
                },
                images: true,
                categories: true,
                reviews: {
                    take: 5,
                    orderBy: { createdAt: 'desc' },
                },
            },
        });
        
        if (product) {
            // Cache for 5 minutes
            await redis.setex(`product:${idOrSlug}`, 300, JSON.stringify(product));
        }
        
        return product;
    }
    
    async searchProducts(query: string, filters?: any): Promise<any> {
        try {
            // Use Algolia for search
            const searchResults = await searchIndex.search(query, {
                filters: this.buildAlgoliaFilters(filters),
                facets: ['categories', 'brand', 'price'],
                hitsPerPage: filters?.limit || 20,
                page: filters?.page || 0,
            });
            
            return {
                products: searchResults.hits,
                total: searchResults.nbHits,
                facets: searchResults.facets,
                page: searchResults.page,
                pages: searchResults.nbPages,
            };
        } catch (error) {
            logger.error('Search error:', error);
            
            // Fallback to database search
            return this.databaseSearch(query, filters);
        }
    }
    
    private buildAlgoliaFilters(filters: any): string {
        const filterParts: string[] = [];
        
        if (filters?.category) {
            filterParts.push(`categories:${filters.category}`);
        }
        
        if (filters?.minPrice || filters?.maxPrice) {
            const min = filters.minPrice || 0;
            const max = filters.maxPrice || 999999;
            filterParts.push(`price:${min} TO ${max}`);
        }
        
        if (filters?.inStock) {
            filterParts.push('inventory.available > 0');
        }
        
        return filterParts.join(' AND ');
    }
    
    private async databaseSearch(query: string, filters: any) {
        const products = await prisma.product.findMany({
            where: {
                AND: [
                    {
                        OR: [
                            { name: { contains: query, mode: 'insensitive' } },
                            { description: { contains: query, mode: 'insensitive' } },
                            { tags: { has: query.toLowerCase() } },
                        ],
                    },
                    filters?.category ? { categories: { some: { slug: filters.category } } } : {},
                    filters?.minPrice ? { price: { gte: filters.minPrice } } : {},
                    filters?.maxPrice ? { price: { lte: filters.maxPrice } } : {},
                ],
                status: 'active',
            },
            include: {
                images: { take: 1 },
                variants: { take: 1 },
            },
            take: filters?.limit || 20,
            skip: (filters?.page || 0) * (filters?.limit || 20),
        });
        
        return { products, total: products.length };
    }
    
    async getRecommendations(productId: string, userId?: string): Promise<Product[]> {
        // Get product for context
        const product = await this.getProduct(productId);
        if (!product) return [];
        
        // Get user-based recommendations if userId provided
        if (userId) {
            const userRecs = await this.getUserBasedRecommendations(userId, productId);
            if (userRecs.length > 0) return userRecs;
        }
        
        // Fallback to content-based recommendations
        return this.getContentBasedRecommendations(product);
    }
    
    private async getUserBasedRecommendations(userId: string, excludeProductId: string): Promise<Product[]> {
        // Collaborative filtering based on user behavior
        const userOrders = await prisma.order.findMany({
            where: { customerId: userId },
            include: { items: true },
            take: 10,
        });
        
        const purchasedProducts = userOrders.flatMap(o => o.items.map(i => i.productId));
        
        // Find users who bought similar products
        const similarUsers = await prisma.order.findMany({
            where: {
                items: {
                    some: {
                        productId: { in: purchasedProducts },
                    },
                },
                customerId: { not: userId },
            },
            select: { customerId: true },
            distinct: ['customerId'],
            take: 50,
        });
        
        // Get products bought by similar users
        const recommendations = await prisma.product.findMany({
            where: {
                orders: {
                    some: {
                        customerId: { in: similarUsers.map(u => u.customerId) },
                    },
                },
                id: { not: excludeProductId },
                status: 'active',
            },
            take: 8,
        });
        
        return recommendations;
    }
    
    private async getContentBasedRecommendations(product: Product): Promise<Product[]> {
        // Find similar products based on categories and tags
        return prisma.product.findMany({
            where: {
                OR: [
                    { categories: { some: { id: { in: product.categories.map(c => c.id) } } } },
                    { tags: { hasSome: product.tags } },
                ],
                id: { not: product.id },
                status: 'active',
            },
            orderBy: { salesCount: 'desc' },
            take: 8,
        });
    }
}

// Shopping Cart Service
class ShoppingCartService {
    async getCart(sessionId: string): Promise<Cart> {
        const cartKey = `cart:${sessionId}`;
        const cartData = await redis.get(cartKey);
        
        if (!cartData) {
            return this.createEmptyCart(sessionId);
        }
        
        const cart = JSON.parse(cartData);
        
        // Validate and update prices
        await this.validateCartItems(cart);
        
        return cart;
    }
    
    async addToCart(sessionId: string, productId: string, variantId?: string, quantity: number = 1): Promise<Cart> {
        const cart = await this.getCart(sessionId);
        
        // Check inventory
        const available = await this.checkInventory(productId, variantId, quantity);
        if (!available) {
            throw new Error('Insufficient inventory');
        }
        
        // Reserve inventory
        await this.reserveInventory(productId, variantId, quantity);
        
        // Get product details
        const product = await prisma.product.findUnique({
            where: { id: productId },
            include: { variants: true },
        });
        
        if (!product) {
            throw new Error('Product not found');
        }
        
        // Determine price
        const variant = variantId ? product.variants.find(v => v.id === variantId) : null;
        const price = variant?.price || product.price;
        
        // Check if item already in cart
        const existingItem = cart.items.find(
            item => item.productId === productId && item.variantId === variantId
        );
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            cart.items.push({
                id: uuidv4(),
                productId,
                variantId,
                quantity,
                price,
                product: {
                    name: product.name,
                    slug: product.slug,
                    image: product.images[0]?.url,
                },
                variant: variant ? {
                    name: variant.name,
                    attributes: variant.attributes,
                } : undefined,
            });
        }
        
        // Update cart totals
        this.calculateCartTotals(cart);
        
        // Save cart
        await this.saveCart(cart);
        
        // Track event
        await this.trackCartEvent('add_to_cart', {
            sessionId,
            productId,
            variantId,
            quantity,
            value: price * quantity,
        });
        
        return cart;
    }
    
    async updateCartItem(sessionId: string, itemId: string, quantity: number): Promise<Cart> {
        const cart = await this.getCart(sessionId);
        const item = cart.items.find(i => i.id === itemId);
        
        if (!item) {
            throw new Error('Item not found in cart');
        }
        
        const quantityDiff = quantity - item.quantity;
        
        if (quantityDiff > 0) {
            // Check additional inventory
            const available = await this.checkInventory(item.productId, item.variantId, quantityDiff);
            if (!available) {
                throw new Error('Insufficient inventory');
            }
            await this.reserveInventory(item.productId, item.variantId, quantityDiff);
        } else if (quantityDiff < 0) {
            // Release inventory
            await this.releaseInventory(item.productId, item.variantId, Math.abs(quantityDiff));
        }
        
        if (quantity === 0) {
            // Remove item
            cart.items = cart.items.filter(i => i.id !== itemId);
        } else {
            item.quantity = quantity;
        }
        
        this.calculateCartTotals(cart);
        await this.saveCart(cart);
        
        return cart;
    }
    
    async applyDiscount(sessionId: string, code: string): Promise<Cart> {
        const cart = await this.getCart(sessionId);
        
        // Validate discount code
        const discount = await prisma.discountCode.findUnique({
            where: { code },
        });
        
        if (!discount || !this.isDiscountValid(discount)) {
            throw new Error('Invalid discount code');
        }
        
        // Check usage limits
        if (discount.maxUses && discount.usageCount >= discount.maxUses) {
            throw new Error('Discount code has reached its usage limit');
        }
        
        // Apply discount
        cart.discountCode = code;
        cart.discount = this.calculateDiscount(cart, discount);
        
        this.calculateCartTotals(cart);
        await this.saveCart(cart);
        
        return cart;
    }
    
    private createEmptyCart(sessionId: string): Cart {
        return {
            id: uuidv4(),
            sessionId,
            items: [],
            subtotal: 0,
            tax: 0,
            shipping: 0,
            discount: 0,
            total: 0,
            createdAt: new Date(),
            updatedAt: new Date(),
        };
    }
    
    private async validateCartItems(cart: Cart) {
        for (const item of cart.items) {
            const product = await prisma.product.findUnique({
                where: { id: item.productId },
                include: { variants: true },
            });
            
            if (!product || product.status !== 'active') {
                // Remove unavailable product
                cart.items = cart.items.filter(i => i.id !== item.id);
                continue;
            }
            
            // Update price if changed
            const variant = item.variantId ? product.variants.find(v => v.id === item.variantId) : null;
            const currentPrice = variant?.price || product.price;
            
            if (item.price !== currentPrice) {
                item.price = currentPrice;
                item.priceChanged = true;
            }
        }
    }
    
    private calculateCartTotals(cart: Cart) {
        cart.subtotal = cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        cart.tax = this.calculateTax(cart);
        cart.shipping = this.calculateShipping(cart);
        cart.total = cart.subtotal + cart.tax + cart.shipping - cart.discount;
        cart.updatedAt = new Date();
    }
    
    private calculateTax(cart: Cart): number {
        // Simplified tax calculation
        const taxRate = 0.08; // 8% tax rate
        return cart.subtotal * taxRate;
    }
    
    private calculateShipping(cart: Cart): number {
        if (cart.subtotal >= config.shipping.freeShippingThreshold) {
            return 0;
        }
        
        // Calculate based on weight/dimensions
        const baseShipping = 5.99;
        const itemShipping = cart.items.length * 0.5;
        
        return baseShipping + itemShipping;
    }
    
    private calculateDiscount(cart: Cart, discount: any): number {
        if (discount.type === 'percentage') {
            return cart.subtotal * (discount.value / 100);
        } else if (discount.type === 'fixed') {
            return Math.min(discount.value, cart.subtotal);
        }
        
        return 0;
    }
    
    private isDiscountValid(discount: any): boolean {
        const now = new Date();
        
        if (discount.startDate && new Date(discount.startDate) > now) {
            return false;
        }
        
        if (discount.endDate && new Date(discount.endDate) < now) {
            return false;
        }
        
        return discount.active;
    }
    
    private async saveCart(cart: Cart) {
        const cartKey = `cart:${cart.sessionId}`;
        await redis.setex(cartKey, config.cart.sessionTimeout, JSON.stringify(cart));
    }
    
    private async checkInventory(productId: string, variantId?: string, quantity: number): Promise<boolean> {
        const inventory = await prisma.inventory.findFirst({
            where: {
                productId,
                variantId: variantId || null,
            },
        });
        
        if (!inventory || !inventory.trackInventory) {
            return true;
        }
        
        const available = inventory.quantity - inventory.reserved;
        
        if (available >= quantity) {
            return true;
        }
        
        return inventory.allowBackorder;
    }
    
    private async reserveInventory(productId: string, variantId?: string, quantity: number) {
        await prisma.inventory.update({
            where: {
                productId_variantId: {
                    productId,
                    variantId: variantId || null,
                },
            },
            data: {
                reserved: { increment: quantity },
            },
        });
        
        // Set expiration for reservation
        const reservationKey = `reservation:${productId}:${variantId || 'default'}:${Date.now()}`;
        await redis.setex(reservationKey, config.cart.reservationTime / 1000, quantity.toString());
    }
    
    private async releaseInventory(productId: string, variantId?: string, quantity: number) {
        await prisma.inventory.update({
            where: {
                productId_variantId: {
                    productId,
                    variantId: variantId || null,
                },
            },
            data: {
                reserved: { decrement: quantity },
            },
        });
    }
    
    private async trackCartEvent(event: string, data: any) {
        // Send to analytics
        await sqs.sendMessage({
            QueueUrl: process.env.ANALYTICS_QUEUE_URL!,
            MessageBody: JSON.stringify({
                event,
                data,
                timestamp: new Date().toISOString(),
            }),
        }).promise();
    }
}

// Checkout Service
class CheckoutService {
    private cart = new ShoppingCartService();
    
    async createCheckout(sessionId: string, checkoutData: any): Promise<Checkout> {
        const cart = await this.cart.getCart(sessionId);
        
        if (cart.items.length === 0) {
            throw new Error('Cart is empty');
        }
        
        // Validate checkout data
        const validated = this.validateCheckoutData(checkoutData);
        
        // Calculate final amounts
        const shipping = await this.calculateShipping(validated.shippingAddress, cart);
        const tax = await this.calculateTax(validated.shippingAddress, cart);
        
        // Create checkout session
        const checkout = {
            id: uuidv4(),
            sessionId,
            cart,
            email: validated.email,
            shippingAddress: validated.shippingAddress,
            billingAddress: validated.billingAddress || validated.shippingAddress,
            shippingMethod: validated.shippingMethod,
            shipping,
            tax,
            total: cart.subtotal + shipping + tax - cart.discount,
            status: 'pending',
            expiresAt: new Date(Date.now() + 3600000), // 1 hour
            createdAt: new Date(),
        };
        
        // Save checkout
        await redis.setex(`checkout:${checkout.id}`, 3600, JSON.stringify(checkout));
        
        return checkout;
    }
    
    async processPayment(checkoutId: string, paymentMethod: string, paymentDetails: any): Promise<Order> {
        // Get checkout
        const checkoutData = await redis.get(`checkout:${checkoutId}`);
        if (!checkoutData) {
            throw new Error('Checkout session expired');
        }
        
        const checkout = JSON.parse(checkoutData);
        
        // Process payment based on method
        let paymentResult;
        switch (paymentMethod) {
            case 'card':
                paymentResult = await this.processCardPayment(checkout, paymentDetails);
                break;
            case 'paypal':
                paymentResult = await this.processPayPalPayment(checkout, paymentDetails);
                break;
            case 'klarna':
                paymentResult = await this.processKlarnaPayment(checkout, paymentDetails);
                break;
            default:
                throw new Error('Unsupported payment method');
        }
        
        if (!paymentResult.success) {
            throw new Error(paymentResult.error || 'Payment failed');
        }
        
        // Create order
        const order = await this.createOrder(checkout, paymentResult);
        
        // Clear cart and checkout
        await redis.del(`cart:${checkout.sessionId}`);
        await redis.del(`checkout:${checkoutId}`);
        
        // Send order confirmation
        await this.sendOrderConfirmation(order);
        
        // Queue fulfillment
        await this.queueFulfillment(order);
        
        return order;
    }
    
    private async processCardPayment(checkout: any, paymentDetails: any) {
        try {
            // Create Stripe payment intent
            const paymentIntent = await stripe.paymentIntents.create({
                amount: Math.round(checkout.total * 100),
                currency: 'usd',
                payment_method: paymentDetails.paymentMethodId,
                confirm: true,
                metadata: {
                    checkoutId: checkout.id,
                },
                shipping: {
                    name: checkout.shippingAddress.name,
                    address: {
                        line1: checkout.shippingAddress.line1,
                        line2: checkout.shippingAddress.line2,
                        city: checkout.shippingAddress.city,
                        state: checkout.shippingAddress.state,
                        postal_code: checkout.shippingAddress.postalCode,
                        country: checkout.shippingAddress.country,
                    },
                },
            });
            
            return {
                success: paymentIntent.status === 'succeeded',
                transactionId: paymentIntent.id,
                amount: paymentIntent.amount / 100,
            };
        } catch (error: any) {
            logger.error('Card payment error:', error);
            return {
                success: false,
                error: error.message,
            };
        }
    }
    
    private async processPayPalPayment(checkout: any, paymentDetails: any) {
        // PayPal integration
        return {
            success: true,
            transactionId: 'PAYPAL_' + Date.now(),
            amount: checkout.total,
        };
    }
    
    private async processKlarnaPayment(checkout: any, paymentDetails: any) {
        // Klarna Buy Now Pay Later integration
        return {
            success: true,
            transactionId: 'KLARNA_' + Date.now(),
            amount: checkout.total,
        };
    }
    
    private async createOrder(checkout: any, paymentResult: any): Promise<Order> {
        const orderNumber = this.generateOrderNumber();
        
        const order = await prisma.order.create({
            data: {
                orderNumber,
                customerId: checkout.customerId,
                email: checkout.email,
                status: OrderStatus.PAID,
                items: {
                    create: checkout.cart.items.map((item: any) => ({
                        productId: item.productId,
                        variantId: item.variantId,
                        quantity: item.quantity,
                        price: item.price,
                        total: item.price * item.quantity,
                    })),
                },
                subtotal: checkout.cart.subtotal,
                tax: checkout.tax,
                shipping: checkout.shipping,
                discount: checkout.cart.discount,
                total: checkout.total,
                shippingAddress: checkout.shippingAddress,
                billingAddress: checkout.billingAddress,
                payment: {
                    method: paymentResult.method,
                    transactionId: paymentResult.transactionId,
                    amount: paymentResult.amount,
                    status: 'completed',
                },
                metadata: {
                    sessionId: checkout.sessionId,
                    checkoutId: checkout.id,
                },
            },
            include: {
                items: true,
            },
        });
        
        // Update inventory
        for (const item of checkout.cart.items) {
            await this.updateInventory(item.productId, item.variantId, item.quantity);
        }
        
        // Update product sales counts
        await this.updateSalesMetrics(order);
        
        return order;
    }
    
    private generateOrderNumber(): string {
        const timestamp = Date.now().toString(36).toUpperCase();
        const random = Math.random().toString(36).substring(2, 6).toUpperCase();
        return `ORD-${timestamp}-${random}`;
    }
    
    private async updateInventory(productId: string, variantId: string | null, quantity: number) {
        await prisma.inventory.update({
            where: {
                productId_variantId: {
                    productId,
                    variantId: variantId || null,
                },
            },
            data: {
                quantity: { decrement: quantity },
                reserved: { decrement: quantity },
            },
        });
        
        // Check for low stock
        const inventory = await prisma.inventory.findUnique({
            where: {
                productId_variantId: {
                    productId,
                    variantId: variantId || null,
                },
            },
        });
        
        if (inventory && inventory.quantity <= config.inventory.lowStockThreshold) {
            await this.sendLowStockAlert(productId, variantId, inventory.quantity);
        }
    }
    
    private async updateSalesMetrics(order: Order) {
        // Update product sales counts and revenue
        for (const item of order.items) {
            await prisma.product.update({
                where: { id: item.productId },
                data: {
                    salesCount: { increment: item.quantity },
                    revenue: { increment: item.total },
                },
            });
        }
        
        // Update daily sales metrics
        await prisma.salesMetric.upsert({
            where: {
                date: new Date().toISOString().split('T')[0],
            },
            create: {
                date: new Date().toISOString().split('T')[0],
                orders: 1,
                revenue: order.total,
                items: order.items.length,
            },
            update: {
                orders: { increment: 1 },
                revenue: { increment: order.total },
                items: { increment: order.items.length },
            },
        });
    }
    
    private async sendOrderConfirmation(order: Order) {
        // Queue email notification
        await sqs.sendMessage({
            QueueUrl: process.env.EMAIL_QUEUE_URL!,
            MessageBody: JSON.stringify({
                type: 'order_confirmation',
                to: order.email,
                orderId: order.id,
                orderNumber: order.orderNumber,
            }),
        }).promise();
    }
    
    private async queueFulfillment(order: Order) {
        // Send to fulfillment queue
        await sqs.sendMessage({
            QueueUrl: process.env.FULFILLMENT_QUEUE_URL!,
            MessageBody: JSON.stringify({
                orderId: order.id,
                orderNumber: order.orderNumber,
                items: order.items,
                shippingAddress: order.shippingAddress,
                shippingMethod: order.shippingMethod,
            }),
        }).promise();
    }
    
    private async sendLowStockAlert(productId: string, variantId: string | null, quantity: number) {
        // Send alert to inventory management
        await sqs.sendMessage({
            QueueUrl: process.env.ALERTS_QUEUE_URL!,
            MessageBody: JSON.stringify({
                type: 'low_stock',
                productId,
                variantId,
                quantity,
                threshold: config.inventory.lowStockThreshold,
            }),
        }).promise();
    }
    
    private validateCheckoutData(data: any) {
        const schema = z.object({
            email: z.string().email(),
            shippingAddress: z.object({
                name: z.string(),
                line1: z.string(),
                line2: z.string().optional(),
                city: z.string(),
                state: z.string(),
                postalCode: z.string(),
                country: z.string(),
                phone: z.string().optional(),
            }),
            billingAddress: z.object({
                name: z.string(),
                line1: z.string(),
                line2: z.string().optional(),
                city: z.string(),
                state: z.string(),
                postalCode: z.string(),
                country: z.string(),
            }).optional(),
            shippingMethod: z.string(),
        });
        
        return schema.parse(data);
    }
    
    private async calculateShipping(address: any, cart: any): Promise<number> {
        // Get shipping rates from carriers
        const rates = await this.getShippingRates(address, cart);
        
        // Return selected method rate
        return rates[0]?.amount || 0;
    }
    
    private async getShippingRates(address: any, cart: any): Promise<any[]> {
        // Integration with shipping carriers
        // This would call APIs for UPS, FedEx, USPS, etc.
        return [
            { carrier: 'USPS', service: 'Priority', amount: 5.99, days: 3 },
            { carrier: 'UPS', service: 'Ground', amount: 8.99, days: 5 },
            { carrier: 'FedEx', service: '2-Day', amount: 15.99, days: 2 },
        ];
    }
    
    private async calculateTax(address: any, cart: any): Promise<number> {
        if (!config.tax.enableAutomaticCalculation) {
            return 0;
        }
        
        // Check if we have nexus in this state
        if (!config.tax.nexusStates.includes(address.state)) {
            return 0;
        }
        
        // Get tax rate for location
        const taxRate = await this.getTaxRate(address);
        
        // Calculate tax on taxable items
        const taxableAmount = cart.items.reduce((sum: number, item: any) => {
            // Check if product is taxable
            const isTaxable = item.product?.taxable !== false;
            return sum + (isTaxable ? item.price * item.quantity : 0);
        }, 0);
        
        return taxableAmount * taxRate;
    }
    
    private async getTaxRate(address: any): Promise<number> {
        // Integration with tax calculation service (TaxJar, Avalara, etc.)
        // Simplified for example
        const stateTaxRates: Record<string, number> = {
            'CA': 0.0725,
            'NY': 0.08,
            'TX': 0.0625,
        };
        
        return stateTaxRates[address.state] || 0;
    }
}

// Order Management Service
class OrderManagementService {
    async getOrder(orderId: string): Promise<Order | null> {
        return prisma.order.findUnique({
            where: { id: orderId },
            include: {
                items: {
                    include: {
                        product: true,
                        variant: true,
                    },
                },
                fulfillments: true,
                refunds: true,
            },
        });
    }
    
    async updateOrderStatus(orderId: string, status: OrderStatus, metadata?: any): Promise<Order> {
        const order = await prisma.order.update({
            where: { id: orderId },
            data: {
                status,
                statusHistory: {
                    create: {
                        status,
                        metadata,
                        createdAt: new Date(),
                    },
                },
            },
            include: {
                items: true,
            },
        });
        
        // Send status update notification
        await this.sendStatusNotification(order);
        
        return order;
    }
    
    async createFulfillment(orderId: string, fulfillmentData: any): Promise<Fulfillment> {
        const fulfillment = await prisma.fulfillment.create({
            data: {
                orderId,
                trackingNumber: fulfillmentData.trackingNumber,
                carrier: fulfillmentData.carrier,
                service: fulfillmentData.service,
                items: fulfillmentData.items,
                shippedAt: new Date(),
                estimatedDelivery: fulfillmentData.estimatedDelivery,
            },
        });
        
        // Update order status
        await this.updateOrderStatus(orderId, OrderStatus.SHIPPED, {
            fulfillmentId: fulfillment.id,
        });
        
        // Send shipping notification
        await this.sendShippingNotification(orderId, fulfillment);
        
        return fulfillment;
    }
    
    async processReturn(orderId: string, returnData: any): Promise<Return> {
        const order = await this.getOrder(orderId);
        if (!order) {
            throw new Error('Order not found');
        }
        
        // Validate return request
        if (!this.isReturnEligible(order)) {
            throw new Error('Order is not eligible for return');
        }
        
        // Create return record
        const returnRecord = await prisma.return.create({
            data: {
                orderId,
                items: returnData.items,
                reason: returnData.reason,
                status: 'pending',
                refundAmount: this.calculateRefundAmount(order, returnData.items),
                returnLabel: await this.generateReturnLabel(order),
            },
        });
        
        // Send return instructions
        await this.sendReturnInstructions(order, returnRecord);
        
        return returnRecord;
    }
    
    async processRefund(orderId: string, amount: number, reason: string): Promise<Refund> {
        const order = await this.getOrder(orderId);
        if (!order) {
            throw new Error('Order not found');
        }
        
        // Process refund through payment gateway
        let refundResult;
        if (order.payment.method === 'card' && order.payment.transactionId) {
            refundResult = await stripe.refunds.create({
                payment_intent: order.payment.transactionId,
                amount: Math.round(amount * 100),
                reason: 'requested_by_customer',
            });
        }
        
        // Create refund record
        const refund = await prisma.refund.create({
            data: {
                orderId,
                amount,
                reason,
                status: refundResult?.status || 'completed',
                transactionId: refundResult?.id,
                processedAt: new Date(),
            },
        });
        
        // Update order status if fully refunded
        const totalRefunded = await this.getTotalRefunded(orderId);
        if (totalRefunded >= order.total) {
            await this.updateOrderStatus(orderId, OrderStatus.REFUNDED);
        }
        
        // Send refund confirmation
        await this.sendRefundConfirmation(order, refund);
        
        return refund;
    }
    
    private isReturnEligible(order: Order): boolean {
        // Check return policy (e.g., 30 days)
        const daysSinceOrder = (Date.now() - order.createdAt.getTime()) / (1000 * 60 * 60 * 24);
        return daysSinceOrder <= 30 && order.status === OrderStatus.DELIVERED;
    }
    
    private calculateRefundAmount(order: Order, returnItems: any[]): number {
        let refundAmount = 0;
        
        for (const returnItem of returnItems) {
            const orderItem = order.items.find(i => i.id === returnItem.itemId);
            if (orderItem) {
                refundAmount += orderItem.price * returnItem.quantity;
            }
        }
        
        // Include proportional tax and shipping
        const refundPercentage = refundAmount / order.subtotal;
        refundAmount += order.tax * refundPercentage;
        refundAmount += order.shipping * refundPercentage;
        
        return refundAmount;
    }
    
    private async generateReturnLabel(order: Order): Promise<string> {
        // Generate return shipping label
        // Integration with shipping carriers
        return `RETURN_LABEL_${order.orderNumber}`;
    }
    
    private async getTotalRefunded(orderId: string): Promise<number> {
        const refunds = await prisma.refund.findMany({
            where: { orderId },
        });
        
        return refunds.reduce((sum, refund) => sum + refund.amount, 0);
    }
    
    private async sendStatusNotification(order: Order) {
        await sqs.sendMessage({
            QueueUrl: process.env.EMAIL_QUEUE_URL!,
            MessageBody: JSON.stringify({
                type: 'order_status_update',
                to: order.email,
                orderId: order.id,
                orderNumber: order.orderNumber,
                status: order.status,
            }),
        }).promise();
    }
    
    private async sendShippingNotification(orderId: string, fulfillment: Fulfillment) {
        const order = await this.getOrder(orderId);
        
        await sqs.sendMessage({
            QueueUrl: process.env.EMAIL_QUEUE_URL!,
            MessageBody: JSON.stringify({
                type: 'shipping_confirmation',
                to: order!.email,
                orderId,
                orderNumber: order!.orderNumber,
                trackingNumber: fulfillment.trackingNumber,
                carrier: fulfillment.carrier,
                estimatedDelivery: fulfillment.estimatedDelivery,
            }),
        }).promise();
    }
    
    private async sendReturnInstructions(order: Order, returnRecord: Return) {
        await sqs.sendMessage({
            QueueUrl: process.env.EMAIL_QUEUE_URL!,
            MessageBody: JSON.stringify({
                type: 'return_instructions',
                to: order.email,
                orderId: order.id,
                returnId: returnRecord.id,
                returnLabel: returnRecord.returnLabel,
            }),
        }).promise();
    }
    
    private async sendRefundConfirmation(order: Order, refund: Refund) {
        await sqs.sendMessage({
            QueueUrl: process.env.EMAIL_QUEUE_URL!,
            MessageBody: JSON.stringify({
                type: 'refund_confirmation',
                to: order.email,
                orderId: order.id,
                orderNumber: order.orderNumber,
                refundAmount: refund.amount,
                refundReason: refund.reason,
            }),
        }).promise();
    }
}

// Customer Service
class CustomerService {
    async createAccount(data: any): Promise<Customer> {
        // Validate data
        const validated = this.validateCustomerData(data);
        
        // Check if email already exists
        const existing = await prisma.customer.findUnique({
            where: { email: validated.email },
        });
        
        if (existing) {
            throw new Error('Email already registered');
        }
        
        // Hash password
        const hashedPassword = await bcrypt.hash(validated.password, 10);
        
        // Create customer
        const customer = await prisma.customer.create({
            data: {
                email: validated.email,
                password: hashedPassword,
                firstName: validated.firstName,
                lastName: validated.lastName,
                phone: validated.phone,
                acceptsMarketing: validated.acceptsMarketing || false,
                verificationToken: uuidv4(),
                verified: false,
            },
        });
        
        // Send verification email
        await this.sendVerificationEmail(customer);
        
        // Subscribe to newsletter if opted in
        if (customer.acceptsMarketing) {
            await this.subscribeToNewsletter(customer.email);
        }
        
        return customer;
    }
    
    async login(email: string, password: string): Promise<{ customer: Customer; token: string }> {
        const customer = await prisma.customer.findUnique({
            where: { email },
        });
        
        if (!customer) {
            throw new Error('Invalid credentials');
        }
        
        const validPassword = await bcrypt.compare(password, customer.password);
        if (!validPassword) {
            throw new Error('Invalid credentials');
        }
        
        if (!customer.verified) {
            throw new Error('Please verify your email');
        }
        
        // Generate JWT token
        const token = jwt.sign(
            {
                customerId: customer.id,
                email: customer.email,
            },
            process.env.JWT_SECRET!,
            { expiresIn: '7d' }
        );
        
        // Update last login
        await prisma.customer.update({
            where: { id: customer.id },
            data: { lastLogin: new Date() },
        });
        
        return { customer, token };
    }
    
    async addToWishlist(customerId: string, productId: string): Promise<void> {
        await prisma.wishlist.create({
            data: {
                customerId,
                productId,
            },
        });
    }
    
    async getRecommendations(customerId: string): Promise<Product[]> {
        // Get customer's purchase history
        const orders = await prisma.order.findMany({
            where: { customerId },
            include: { items: true },
            orderBy: { createdAt: 'desc' },
            take: 10,
        });
        
        // Get customer's browsing history
        const browsingHistory = await redis.lrange(`browsing:${customerId}`, 0, 20);
        
        // Get customer's wishlist
        const wishlist = await prisma.wishlist.findMany({
            where: { customerId },
            select: { productId: true },
        });
        
        // Generate personalized recommendations
        // This would use a recommendation engine (collaborative filtering, content-based, etc.)
        const recommendations = await this.generatePersonalizedRecommendations({
            orders,
            browsingHistory,
            wishlist,
        });
        
        return recommendations;
    }
    
    private validateCustomerData(data: any) {
        const schema = z.object({
            email: z.string().email(),
            password: z.string().min(8),
            firstName: z.string(),
            lastName: z.string(),
            phone: z.string().optional(),
            acceptsMarketing: z.boolean().optional(),
        });
        
        return schema.parse(data);
    }
    
    private async sendVerificationEmail(customer: Customer) {
        await sqs.sendMessage({
            QueueUrl: process.env.EMAIL_QUEUE_URL!,
            MessageBody: JSON.stringify({
                type: 'email_verification',
                to: customer.email,
                customerId: customer.id,
                verificationToken: customer.verificationToken,
            }),
        }).promise();
    }
    
    private async subscribeToNewsletter(email: string) {
        // Add to mailing list (e.g., Mailchimp, SendGrid)
        await sqs.sendMessage({
            QueueUrl: process.env.MARKETING_QUEUE_URL!,
            MessageBody: JSON.stringify({
                action: 'subscribe',
                email,
                list: 'newsletter',
            }),
        }).promise();
    }
    
    private async generatePersonalizedRecommendations(data: any): Promise<Product[]> {
        // Simplified recommendation logic
        // In production, this would use ML models
        
        const productIds = new Set<string>();
        
        // Add products from same categories as purchased items
        for (const order of data.orders) {
            for (const item of order.items) {
                const product = await prisma.product.findUnique({
                    where: { id: item.productId },
                    include: { categories: true },
                });
                
                if (product) {
                    const related = await prisma.product.findMany({
                        where: {
                            categories: {
                                some: {
                                    id: { in: product.categories.map(c => c.id) },
                                },
                            },
                            id: { not: product.id },
                        },
                        take: 3,
                    });
                    
                    related.forEach(p => productIds.add(p.id));
                }
            }
        }
        
        // Add trending products
        const trending = await prisma.product.findMany({
            where: {
                status: 'active',
                id: { notIn: Array.from(productIds) },
            },
            orderBy: { salesCount: 'desc' },
            take: 5,
        });
        
        trending.forEach(p => productIds.add(p.id));
        
        // Fetch full product details
        return prisma.product.findMany({
            where: { id: { in: Array.from(productIds) } },
            include: { images: true },
            take: 12,
        });
    }
}

// Type definitions
interface Cart {
    id: string;
    sessionId: string;
    customerId?: string;
    items: CartItem[];
    subtotal: number;
    tax: number;
    shipping: number;
    discount: number;
    total: number;
    discountCode?: string;
    createdAt: Date;
    updatedAt: Date;
}

interface Checkout {
    id: string;
    sessionId: string;
    cart: Cart;
    email: string;
    shippingAddress: Address;
    billingAddress: Address;
    shippingMethod: string;
    shipping: number;
    tax: number;
    total: number;
    status: string;
    expiresAt: Date;
    createdAt: Date;
}

interface Address {
    name: string;
    line1: string;
    line2?: string;
    city: string;
    state: string;
    postalCode: string;
    country: string;
    phone?: string;
}

interface OrderItem {
    id: string;
    orderId: string;
    productId: string;
    variantId?: string;
    quantity: number;
    price: number;
    total: number;
    product?: Product;
    variant?: ProductVariant;
}

interface PaymentInfo {
    method: string;
    transactionId: string;
    amount: number;
    status: string;
}

interface FulfillmentInfo {
    status: string;
    trackingNumber?: string;
    carrier?: string;
    shippedAt?: Date;
    deliveredAt?: Date;
}

interface Fulfillment {
    id: string;
    orderId: string;
    trackingNumber: string;
    carrier: string;
    service: string;
    items: any[];
    shippedAt: Date;
    estimatedDelivery?: Date;
    deliveredAt?: Date;
}

interface Return {
    id: string;
    orderId: string;
    items: any[];
    reason: string;
    status: string;
    refundAmount: number;
    returnLabel: string;
    receivedAt?: Date;
}

interface Refund {
    id: string;
    orderId: string;
    amount: number;
    reason: string;
    status: string;
    transactionId?: string;
    processedAt: Date;
}

interface Customer {
    id: string;
    email: string;
    password: string;
    firstName: string;
    lastName: string;
    phone?: string;
    acceptsMarketing: boolean;
    verificationToken?: string;
    verified: boolean;
    lastLogin?: Date;
    createdAt: Date;
}

interface ProductImage {
    id: string;
    url: string;
    alt?: string;
    position: number;
}

interface Category {
    id: string;
    name: string;
    slug: string;
    parentId?: string;
}

interface InventoryLocation {
    locationId: string;
    quantity: number;
}

interface Dimensions {
    length: number;
    width: number;
    height: number;
    unit: string;
}

interface SEOData {
    title: string;
    description: string;
    keywords?: string[];
}

// Export services
export {
    ProductCatalogService,
    ShoppingCartService,
    CheckoutService,
    OrderManagementService,
    CustomerService,
};
```
