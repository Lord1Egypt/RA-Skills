// Node.js wrapper: 通过 stdin 接收 s 值，返回 X-Bogus sign
// 用 eval 加载 sign.js 使 get_sign 进入作用域
const fs = require('fs');
const path = require('path');
const signCode = fs.readFileSync(path.join(__dirname, 'sign.js'), 'utf8');
eval(signCode);

process.stdin.setEncoding('utf8');
let input = '';
process.stdin.on('data', (chunk) => { input += chunk; });
process.stdin.on('end', () => {
    const s = input.trim();
    const result = get_sign(s);
    process.stdout.write(String(result));
});
