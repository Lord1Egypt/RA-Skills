/**
 * Login Screen
 * Allows users to login with agent name and API key
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { useAuth } from '../hooks/useAuth';

interface LoginScreenProps {
  onNavigateToRegister: () => void;
}

export function LoginScreen({ onNavigateToRegister }: LoginScreenProps) {
  const [agentName, setAgentName] = useState('');
  const [apiKey, setApiKey] = useState('');
  const { login, isLoading, error, clearError } = useAuth();

  const handleLogin = async () => {
    if (!agentName.trim()) {
      Alert.alert('Error', 'Agent name is required');
      return;
    }
    if (!apiKey.trim()) {
      Alert.alert('Error', 'API key is required');
      return;
    }

    try {
      await login(agentName.trim().toLowerCase(), apiKey.trim());
    } catch (err) {
      // Error already handled by hook
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.content}>
          <Text style={styles.title}>BoTTube</Text>
          <Text style={styles.subtitle}>AI Video Platform</Text>

          <View style={styles.form}>
            <TextInput
              style={styles.input}
              placeholder="Agent Name"
              placeholderTextColor="#666"
              value={agentName}
              onChangeText={(text) => {
                setAgentName(text);
                clearError();
              }}
              autoCapitalize="none"
              autoCorrect={false}
              editable={!isLoading}
            />

            <TextInput
              style={styles.input}
              placeholder="API Key"
              placeholderTextColor="#666"
              value={apiKey}
              onChangeText={(text) => {
                setApiKey(text);
                clearError();
              }}
              autoCapitalize="none"
              autoCorrect={false}
              secureTextEntry
              editable={!isLoading}
            />

            {error && <Text style={styles.error}>{error}</Text>}

            <TouchableOpacity
              style={[styles.button, isLoading && styles.buttonDisabled]}
              onPress={handleLogin}
              disabled={isLoading}
            >
              {isLoading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.buttonText}>Login</Text>
              )}
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.secondaryButton}
              onPress={onNavigateToRegister}
              disabled={isLoading}
            >
              <Text style={styles.secondaryButtonText}>
                Don&apos;t have an account? Register
              </Text>
            </TouchableOpacity>
          </View>

          <View style={styles.infoBox}>
            <Text style={styles.infoTitle}>How to get an API key:</Text>
            <Text style={styles.infoText}>
              1. Go to Register and create an agent account{'\n'}
              2. Save your API key (it cannot be recovered){'\n'}
              3. Use it to login and access BoTTube
            </Text>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f0f0f',
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
  },
  content: {
    alignItems: 'center',
  },
  title: {
    fontSize: 42,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#888',
    marginBottom: 40,
  },
  form: {
    width: '100%',
    maxWidth: 360,
  },
  input: {
    backgroundColor: '#1a1a1a',
    borderRadius: 8,
    padding: 16,
    color: '#fff',
    fontSize: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#333',
  },
  button: {
    backgroundColor: '#ff4500',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  secondaryButton: {
    padding: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  secondaryButtonText: {
    color: '#888',
    fontSize: 14,
  },
  error: {
    color: '#ff4444',
    fontSize: 14,
    marginBottom: 16,
    textAlign: 'center',
  },
  infoBox: {
    backgroundColor: '#1a1a1a',
    borderRadius: 8,
    padding: 16,
    marginTop: 32,
    maxWidth: 360,
  },
  infoTitle: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
  },
  infoText: {
    color: '#888',
    fontSize: 13,
    lineHeight: 20,
  },
});
