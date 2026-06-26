/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: "class",
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
        "./views/**/*.{js,ts,jsx,tsx}",
        "./components/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                "primary": "#722dcd",
                "primary-glow": "#9d5ae3",
                "glass-border": "rgba(255, 255, 255, 0.15)",
                "glass-surface": "rgba(26, 26, 42, 0.4)",
                "background-dark": "#080810",
                "liquid-purple": "#8a3ffc",
                "primary-dark": "#9d4edd",
                "danger": "#ef4444",
                "accent-teal": "#4cc9f0",
                "status-green": "#4ade80",
                "merit-gold": "#ffb703",
                "merit-amber": "#fb8500",
            },
            fontFamily: {
                "display": ["Space Grotesk", "Noto Sans SC", "sans-serif"],
                "body": ["Noto Sans SC", "sans-serif"],
            },
            animation: {
                'pulse-fast': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'float': 'float 6s ease-in-out infinite',
                'shake': 'shake 0.5s cubic-bezier(.36,.07,.19,.97) infinite both',
                'boil': 'boil 2s infinite ease-in-out',
                'ripple': 'ripple 3s linear infinite',
                'scan': 'scan 3s ease-in-out infinite',
                'float-delayed': 'float 12s ease-in-out infinite 5s',
                'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'liquid-spin': 'spin 15s linear infinite',
                'bubble-rise': 'rise 4s ease-in infinite',
                'wave': 'wave 3s ease-in-out infinite',
                'shimmer': 'shimmer 2s linear infinite',
                'flash-urgent': 'flash-urgent 0.8s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'splash': 'splash 0.6s ease-out forwards',
                'liquid-flow': 'liquid-flow 3s ease-in-out infinite',
            },
            keyframes: {
                float: {
                    '0%, 100%': { transform: 'translateY(0) scale(1)' },
                    '50%': { transform: 'translateY(-20px) scale(1.05)' },
                },
                shake: {
                    '10%, 90%': { transform: 'translate3d(-1px, 1px, 0)' },
                    '20%, 80%': { transform: 'translate3d(2px, -1px, 0)' },
                    '30%, 50%, 70%': { transform: 'translate3d(-3px, 2px, 0)' },
                    '40%, 60%': { transform: 'translate3d(3px, -2px, 0)' }
                },
                boil: {
                    '0%, 100%': { transform: 'scale(1)', filter: 'brightness(1)' },
                    '50%': { transform: 'scale(1.02)', filter: 'brightness(1.2)' }
                },
                ripple: {
                    '0%': { transform: 'translate(-50%, -50%) scale(1)', opacity: 0.5 },
                    '100%': { transform: 'translate(-50%, -50%) scale(2)', opacity: 0 }
                },
                scan: {
                    '0%': { transform: 'translateY(-100%)' },
                    '100%': { transform: 'translateY(400%)' }
                },
                rise: {
                    '0%': { transform: 'translateY(100%) scale(0.5)', opacity: '0' },
                    '50%': { opacity: '0.8' },
                    '100%': { transform: 'translateY(-20%) scale(1.2)', opacity: '0' },
                },
                wave: {
                    '0%, 100%': { transform: 'translateX(-5%)' },
                    '50%': { transform: 'translateX(5%)' },
                },
                shimmer: {
                    '0%': { transform: 'translateX(-100%)' },
                    '100%': { transform: 'translateX(100%)' }
                },
                'flash-urgent': {
                    '0%, 100%': { boxShadow: '0 0 5px rgba(220, 38, 38, 0.4)', borderColor: 'rgba(239, 68, 68, 0.3)', backgroundColor: 'rgba(69, 10, 10, 0.6)' },
                    '50%': { boxShadow: '0 0 20px rgba(220, 38, 38, 0.9)', borderColor: 'rgba(239, 68, 68, 0.8)', backgroundColor: 'rgba(127, 29, 29, 0.7)' },
                },
                splash: {
                    '0%': { transform: 'scale(0)', opacity: '0.8' },
                    '100%': { transform: 'scale(4)', opacity: '0' }
                },
                'liquid-flow': {
                    '0%, 100%': { filter: 'hue-rotate(0deg) brightness(1)' },
                    '50%': { filter: 'hue-rotate(15deg) brightness(1.2)' },
                }
            }
        },
    },
    plugins: [],
}
