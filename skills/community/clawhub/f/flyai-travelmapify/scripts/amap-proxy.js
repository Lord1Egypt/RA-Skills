#!/usr/bin/env node

const http = require('http');
const url = require('url');
const { exec } = require('child_process');
const path = require('path');

const PORT = 8769;

// CORS headers
const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
};

// Handle search requests
function handleSearch(query, city, response) {
    // Use relative path to amap-maps skill
    const amapMapsDir = path.join(__dirname, '..', '..', 'amap-maps');
    // Use default API key or allow override via environment variable
    const amapKey = process.env.AMAP_KEY || "88628414733cf2ccb7ce2f94cfd680ef";
    const command = `cd "${amapMapsDir}" && AMAP_KEY="${amapKey}" node scripts/amap.js search text "${query}" ${city}`;
    
    exec(command, { timeout: 10000 }, (error, stdout, stderr) => {
        if (error) {
            console.error('Search error:', error);
            response.writeHead(500, corsHeaders);
            response.end(JSON.stringify({ error: 'Search failed', details: error.message }));
            return;
        }
        
        try {
            const result = JSON.parse(stdout);
            response.writeHead(200, { ...corsHeaders, 'Content-Type': 'application/json' });
            response.end(JSON.stringify(result));
        } catch (parseError) {
            console.error('JSON parse error:', parseError);
            response.writeHead(500, corsHeaders);
            response.end(JSON.stringify({ error: 'Invalid response format' }));
        }
    });
}

// Handle detail requests
function handleDetail(poiId, response) {
    // Use relative path to amap-maps skill
    const amapMapsDir = path.join(__dirname, '..', '..', 'amap-maps');
    // Use default API key or allow override via environment variable
    const amapKey = process.env.AMAP_KEY || "88628414733cf2ccb7ce2f94cfd680ef";
    const command = `cd "${amapMapsDir}" && AMAP_KEY="${amapKey}" node scripts/amap.js search detail "${poiId}"`;
    
    exec(command, { timeout: 10000 }, (error, stdout, stderr) => {
        if (error) {
            console.error('Detail error:', error);
            response.writeHead(500, corsHeaders);
            response.end(JSON.stringify({ error: 'Detail fetch failed' }));
            return;
        }
        
        try {
            const result = JSON.parse(stdout);
            response.writeHead(200, { ...corsHeaders, 'Content-Type': 'application/json' });
            response.end(JSON.stringify(result));
        } catch (parseError) {
            console.error('JSON parse error:', parseError);
            response.writeHead(500, corsHeaders);
            response.end(JSON.stringify({ error: 'Invalid response format' }));
        }
    });
}

// Create HTTP server
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    
    // Handle CORS preflight
    if (req.method === 'OPTIONS') {
        res.writeHead(200, corsHeaders);
        res.end();
        return;
    }
    
    // Handle search endpoint
    if (pathname === '/api/search' && req.method === 'GET') {
        const query = parsedUrl.query.q;
        const city = parsedUrl.query.city || '重庆';
        
        if (!query) {
            res.writeHead(400, corsHeaders);
            res.end(JSON.stringify({ error: 'Query parameter "q" is required' }));
            return;
        }
        
        handleSearch(query, city, res);
        return;
    }
    
    // Handle detail endpoint
    if (pathname.startsWith('/api/detail/') && req.method === 'GET') {
        const poiId = pathname.split('/api/detail/')[1];
        
        if (!poiId) {
            res.writeHead(400, corsHeaders);
            res.end(JSON.stringify({ error: 'POI ID is required' }));
            return;
        }
        
        handleDetail(poiId, res);
        return;
    }
    
    // Handle root endpoint
    if (pathname === '/' && req.method === 'GET') {
        res.writeHead(200, { ...corsHeaders, 'Content-Type': 'text/plain' });
        res.end('AMap Search Proxy running on http://localhost:' + PORT + '\nSearch endpoint: http://localhost:' + PORT + '/api/search?q=解放碑\n');
        return;
    }
    
    // 404 for other routes
    res.writeHead(404, corsHeaders);
    res.end(JSON.stringify({ error: 'Not found' }));
});

server.listen(PORT, () => {
    console.log(`AMap Search Proxy running on http://localhost:${PORT}`);
    console.log(`Search endpoint: http://localhost:${PORT}/api/search?q=解放碑`);
});