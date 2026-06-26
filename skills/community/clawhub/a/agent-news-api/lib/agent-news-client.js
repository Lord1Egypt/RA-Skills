const axios = require('axios');
const io = require('socket.io-client');
const { Keypair } = require('@solana/web3.js');
const nacl = require('tweetnacl');
const bs58 = require('bs58').default || require('bs58');
const EventEmitter = require('events');

class AgentNewsClient extends EventEmitter {
    /**
     * @param {Object} options
     * @param {string} [options.apiKey] - Your Agent News API Key
     * @param {string} [options.privateKey] - Base58 encoded Solana private key for Zero-HITL Auth
     * @param {string} [options.apiUrl] - Base URL for the API (default: https://api.agentnewsapi.com)
     */
    constructor(options = {}) {
        super();
        this.apiKey = options.apiKey || null;
        this.privateKeyBase58 = options.privateKey || null;
        this.apiUrl = options.apiUrl || 'https://api.agentnewsapi.com'; 
        this.socket = null;
        this.isConnected = false;
        this.creditBalance = null;
    }

    /**
     * Connects to the Agent News API and establishes the real-time firehose.
     * If no API key is provided, attempts Zero-HITL authentication using the provided Solana private key.
     */
    async connect() {
        await this._ensureApiKey();
        return this._initializeWebSocket();
    }

    /**
     * Internal helper to ensure we have an API key, via Zero-HITL if necessary.
     */
    async _ensureApiKey() {
        if (!this.apiKey) {
            if (!this.privateKeyBase58) {
                throw new Error('Must provide either an apiKey or a privateKey for Zero-HITL authentication.');
            }
            console.log('[AGENT NEWS] No API key provided. Initiating Zero-HITL Authentication via Solana...');
            this.apiKey = await this._authenticateWithSolana();
            console.log('[AGENT NEWS] Zero-HITL Auth Successful. API Key acquired.');
        }
    }

    /**
     * Disconnects the real-time firehose.
     */
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.isConnected = false;
        }
    }

    /**
     * Fetch the latest curated signals from the REST API.
     * @param {Object} options - { limit: number, q: string }
     * @returns {Promise<Array>}
     */
    async getLatestSignals(options = {}) {
        try {
            const params = { limit: options.limit || 20 };
            if (options.q) params.q = options.q;

            const response = await this._request('get', '/api/news/latest', { params });
            return response.data.articles || [];
        } catch (error) {
            throw new Error(`Failed to fetch latest signals: ${error.response?.data?.error || error.message}`);
        }
    }

    /**
     * Fetch delayed curated signals from the REST API (FREE TIER).
     * Subject to a 20-minute delay and 1 request per minute rate limit.
     * Does NOT require authentication — unauthenticated requests are rate-limited by IP.
     * @param {Object} options - { limit: number, q: string }
     * @returns {Promise<Array>}
     */
    async getFreeSignals(options = {}) {
        try {
            const params = { limit: options.limit || 20 };
            if (options.q) params.q = options.q;

            const headers = {};
            if (this.apiKey) headers['X-API-KEY'] = this.apiKey;

            const response = await axios({
                method: 'get',
                url: `${this.apiUrl}/api/news/free`,
                headers,
                params
            });
            return response.data.articles || [];
        } catch (error) {
            throw new Error(`Failed to fetch free signals: ${error.response?.data?.error || error.message}`);
        }
    }

    /**
     * Fetch current API credit balance.
     * @returns {Promise<number>}
     */
    async getCreditBalance() {
        try {
            const response = await this._request('get', '/api/users/me');
            this.creditBalance = response.data.user?.apiCredits || 0;
            return this.creditBalance;
        } catch (error) {
            throw new Error(`Failed to fetch credit balance: ${error.response?.data?.error || error.message}`);
        }
    }

    // --- Private Methods ---

    /**
     * Internal request helper that handles 401s and silent re-authentication.
     */
    async _request(method, path, options = {}) {
        // Automatically ensure API key if not present (triggers initial auth)
        await this._ensureApiKey();

        const execute = async () => {
            return axios({
                method,
                url: `${this.apiUrl}${path}`,
                headers: { 'X-API-KEY': this.apiKey, ...options.headers },
                params: options.params,
                data: options.data
            });
        };

        try {
            return await execute();
        } catch (error) {
            // Handle expired/invalid key by retrying with fresh Zero-HITL auth
            if (error.response?.status === 401 && this.privateKeyBase58) {
                console.log('[AGENT NEWS] Auth Expired. Attempting Silent Re-Authentication via Solana...');
                this.apiKey = await this._authenticateWithSolana();
                return await execute();
            }
            throw error;
        }
    }

    async _authenticateWithSolana() {
        try {
            // 1. Decode keypair
            const secretKey = bs58.decode(this.privateKeyBase58);
            const keypair = Keypair.fromSecretKey(secretKey);
            const walletAddress = keypair.publicKey.toBase58();

            // 2. Sign auth message
            const message = "Allow Agent News API Access";
            const encodedMessage = new TextEncoder().encode(message);
            const signature = nacl.sign.detached(encodedMessage, secretKey);

            // 3. Request API Key
            const response = await axios.post(`${this.apiUrl}/api/keys/autonomous`, {
                walletAddress,
                signature: bs58.encode(signature),
                message
            });

            if (!response.data.success || !response.data.apiKey) {
                throw new Error('Server rejected Zero-HITL authentication.');
            }

            return response.data.apiKey;
        } catch (error) {
            throw new Error(`Zero-HITL Authentication failed: ${error.response?.data?.error || error.message}`);
        }
    }

    _initializeWebSocket() {
        return new Promise((resolve, reject) => {
            this.socket = io(this.apiUrl, {
                auth: { apiKey: this.apiKey }
            });

            this.socket.on('connect', () => {
                this.isConnected = true;
                this.emit('connected');
                resolve();
            });

            this.socket.on('news_update', (data) => {
                // Update internal balance if meta exists
                if (data._meta && typeof data._meta.remainingCredits === 'number') {
                    this.creditBalance = data._meta.remainingCredits;
                }
                // Emit purely the narrative/signal data
                this.emit('signal', data);
            });

            this.socket.on('balance_update', (data) => {
                this.creditBalance = data.credits;
                this.emit('balance', this.creditBalance);
            });

            this.socket.on('error', (err) => {
                this.emit('error', err);
            });

            this.socket.on('connect_error', (err) => {
                this.isConnected = false;
                reject(new Error(`WebSocket connection failed: ${err.message}`));
            });

            this.socket.on('disconnect', () => {
                this.isConnected = false;
                this.emit('disconnected');
            });
        });
    }

}

module.exports = { AgentNewsClient };
