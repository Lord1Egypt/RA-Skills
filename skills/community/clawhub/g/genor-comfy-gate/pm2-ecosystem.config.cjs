module.exports = {
  apps: [
    {
      name: 'genor-comfy-gate',
      script: 'server.js',
      env: {
        PORT: '8188',
        GATEWAY_PUBLIC_HOST: 'localhost'
      }
    }
  ]
};
