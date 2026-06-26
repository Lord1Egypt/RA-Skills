const cryptico = require('./summer-cryptico-2.0.2.min.js');

try {
    const sc = cryptico.SummerCryptico;

    const u = process.argv[2];
    if (!u) {
        console.error("Error: Please provide a u to encrypt as the first argument.");
        process.exit(1);
    }

    const base64PubKey = process.argv[3];
    if (!base64PubKey) {
        console.error("Error: Please provide a base64PubKey as the second argument.");
        process.exit(1);
    }

    let result = sc.encryptData(base64PubKey, u);

    // Output only the result string directly perfectly for Python
    process.stdout.write(result + '\n');
} catch (e) {
    console.error(e.message);
    process.exit(1);
}
