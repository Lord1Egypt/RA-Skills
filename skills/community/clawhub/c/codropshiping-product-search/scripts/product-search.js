
const https = require('https');

function parseArgs() {
    const args = {};
    process.argv.slice(2).forEach(arg => {
        if (arg.startsWith('--')) {
            const [key, value] = arg.substring(2).split('=');
            args[key] = value;
        }
    });
    return args;
}

const args = parseArgs();
const keyword = args.keyword;
const token = args.token;

if (!keyword) {
    console.error('Please provide a keyword using --keyword=<your_keyword>');
    process.exit(1);
}

if (!token) {
    console.error('Please provide a token using --token=<your_token>');
    process.exit(1);
}

const postData = JSON.stringify({
    keyword: keyword
});

const options = {
    hostname: 'test-codrop.cargosoon.online',
    path: '/api/shipping/Goods/ProductSearchKeywordQuery',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'token': token
    }
};

const req = https.request(options, (res) => {
    let data = '';

    res.on('data', (chunk) => {
        data += chunk;
    });

    res.on('end', () => {
        try {
            const parsedData = JSON.parse(data);
            if (parsedData.code && parsedData.code.toString() !== '0') {
                console.error('API Error:', parsedData.msg);
            } else {
                console.log(JSON.stringify(parsedData.data !== undefined ? parsedData.data : parsedData, null, 2));
            }
        } catch (e) {
            console.error('Failed to parse JSON response from server.');
            console.log('Raw Response:', data);
        }
    });
});

req.on('error', (e) => {
    console.error(`problem with request: ${e.message}`);
});

// Write data to request body
req.write(postData);
req.end();
